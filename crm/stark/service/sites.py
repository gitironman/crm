# __author: iamironman
from django.urls import path, re_path, reverse
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from django.core.exceptions import FieldDoesNotExist
from django.db.models import Q


class ShowList(object):
    def __init__(self, request, config_obj, queryset):
        self.config_obj = config_obj
        self.queryset = queryset
        self.request = request
        self.pager_queryset = self.get_pager_queryset()
        self.table_name = self.config_obj.model._meta.verbose_name

    def get_pager_queryset(self):
        from stark.utils.page import Pagination
        current_page = self.request.GET.get('page', 1)
        self.pagination = Pagination(self.request, current_page, self.queryset,
                                     per_page_num=self.config_obj.per_page_num or 5)
        queryset = self.queryset[self.pagination.start:self.pagination.end]
        return queryset

    def get_header(self):
        header_list = []
        for field_or_func in self.config_obj.get_new_list_display():
            if callable(field_or_func):
                val = field_or_func(self.config_obj, header=True)
                header_list.append(val)
            else:
                if field_or_func == '__str__':
                    val = self.config_obj.model._meta.model_name.upper()
                else:
                    field_obj = self.config_obj.model._meta.get_field(field_or_func)
                    val = field_obj.verbose_name
                header_list.append(val)
        return header_list

    def get_body(self):
        new_data = []
        for obj in self.pager_queryset:
            temp = []

            for field_or_func in self.config_obj.get_new_list_display():
                if callable(field_or_func):
                    val = field_or_func(self.config_obj, obj)
                else:
                    try:
                        from django.db.models.fields.related import ManyToManyField
                        field_obj = self.config_obj.model._meta.get_field(field_or_func)
                        if type(field_obj) == ManyToManyField:
                            raise Exception('list_display不能是多对多字段')
                        if field_obj.choices:
                            val = getattr(obj, 'get_{}_display'.format(field_or_func))()
                        else:
                            val = getattr(obj, field_or_func)
                            if field_or_func in self.config_obj.list_display_links:
                                val = mark_safe("<a href='{}'>{}</a>".format(self.config_obj.get_edit_url(obj), val))
                    except FieldDoesNotExist:
                        val = getattr(obj, field_or_func)()
                temp.append(val)
            new_data.append(temp)
        return new_data


class ModelStark(object):
    list_display = ('__str__',)
    list_display_links = []
    model_form_class = None
    per_page_num = None
    search_fields = []
    search_val = None
    list_filter = []

    def __init__(self, model):
        self.model = model
        self.model_name = self.model._meta.model_name
        self.app_label = self.model._meta.app_label

    def get_list_url(self):
        list_url = reverse('{}_{}_list'.format(self.app_label, self.model_name))
        return list_url

    def get_add_url(self):
        add_url = reverse('{}_{}_add'.format(self.app_label, self.model_name))
        return add_url

    def get_delete_url(self, obj):
        delete_url = reverse('{}_{}_delete'.format(self.app_label, self.model_name), args=(obj.pk,))
        return delete_url

    def get_edit_url(self, obj):
        edit_url = reverse('{}_{}_edit'.format(self.app_label, self.model_name), args=(obj.pk,))
        return edit_url

    def show_checkbox(self, obj=None, header=False):
        if header:
            return mark_safe("<input type='checkbox' name='checkall'>")
        return mark_safe("<input name='_selected_action' value={} type='checkbox'>".format(obj.pk))

    def show_delbtn(self, obj=None, header=False):
        if header:
            return '删除'
        return mark_safe("<a href='{}'>删除</a>".format(self.get_delete_url(obj)))

    def show_editbtn(self, obj=None, header=False):
        if header:
            return '编辑'
        return mark_safe("<a href='{}'>编辑</a>".format(self.get_edit_url(obj)))

    def get_new_list_display(self):
        temp = []
        temp.extend(self.list_display)
        temp.append(ModelStark.show_editbtn)
        temp.append(ModelStark.show_delbtn)
        temp.insert(0, ModelStark.show_checkbox)
        return temp

    def get_search_condition(self, request):
        val = request.GET.get('q')
        q = Q()
        if val:
            self.search_val = val
            q.connector = 'or'
            for field in self.search_fields:
                q.children.append((field + '__contains', val))
        else:
            self.search_val = None
        return q

    def patch_delete(self, request, queryset):
        queryset.delete()

    patch_delete.desc = '批量删除'
    actions = []

    def get_new_actions(self):
        temp = []
        temp.extend(self.actions)
        temp.append(self.patch_delete)
        return temp

    def get_action_dict(self):
        actions_list = []
        for func in self.get_new_actions():
            actions_list.append({
                'name': func.__name__,
                'desc': func.desc,
            })
        return actions_list

    def get_list_filter_links(self):
        list_filter_links = {}
        for filter_field in self.list_filter:
            import copy
            params = copy.deepcopy(self.request.GET)
            current_field_val = params.get(filter_field)
            filter_field_obj = self.model._meta.get_field(filter_field)
            from django.db.models.fields.related import ForeignKey, ManyToManyField
            if isinstance(filter_field_obj, ForeignKey) or isinstance(filter_field_obj, ManyToManyField):
                data = filter_field_obj.remote_field.model.objects.all()
            elif filter_field_obj.choices:
                data = filter_field_obj.choices
            else:
                raise Exception('过滤字段不能为普通字段')
            temp = []
            if params.get(filter_field):
                del params[filter_field]
            all = "<a class='text-muted' href='?{}'>全部</a>".format(params.urlencode())
            temp.append(all)
            for item in data:
                if type(item) == tuple:
                    pk, text = item
                else:
                    pk, text = item.pk, str(item)
                params[filter_field] = pk
                _url = '?{}'.format(params.urlencode())
                if current_field_val == str(pk):
                    link = "<a class='text-primary' href='{}'>{}</a>".format(_url, text)
                else:
                    link = "<a class='text-muted' href='{}'>{}</a>".format(_url, text)
                temp.append(link)
            list_filter_links[filter_field] = temp
        return list_filter_links

    def get_list_filter_condition(self):
        q = Q()
        for filter_field, val in self.request.GET.items():
            if filter_field in ['page', 'q']:
                continue
            q.children.append((filter_field, val))
        return q

    def list_view(self, request):
        self.request = request
        if request.method == 'POST':
            action_func_str = request.POST.get('action')
            if action_func_str:
                action_func = getattr(self, action_func_str)
                _selected_action = request.POST.getlist('_selected_action')
                queryset = self.model.objects.filter(pk__in=_selected_action)
                action_func(request, queryset)
        queryset = self.model.objects.all()
        search_condition = self.get_search_condition(request)
        list_filter_condition = self.get_list_filter_condition()
        queryset = queryset.filter(search_condition).filter(list_filter_condition)
        show_list = ShowList(request, self, queryset)
        add_url = self.get_add_url()
        import datetime
        now = datetime.datetime.now()
        user = request.session.get('user')
        return render(request, 'stark/list_view.html', locals())

    def get_model_form(self):
        from django.forms import ModelForm
        class BaseModelForm(ModelForm):
            class Meta:
                model = self.model
                fields = '__all__'

        return self.model_form_class or BaseModelForm

    def add_view(self, request):
        BaseModelForm = self.get_model_form()
        table_name = self.model._meta.verbose_name
        if request.method == 'GET':
            form_obj = BaseModelForm
            return render(request, 'stark/add_view.html', locals())
        else:
            form_obj = BaseModelForm(request.POST)
            if form_obj.is_valid():
                form_obj.save()
                return redirect(self.get_list_url())
            else:
                return render(request, 'stark/add_view.html', locals())

    def edit_view(self, request, id):
        BaseModeForm = self.get_model_form()
        table_name = self.model._meta.verbose_name
        edit_obj = self.model.objects.filter(pk=id).first()
        if request.method == 'GET':
            form_obj = BaseModeForm(instance=edit_obj)
            return render(request, 'stark/edit_view.html', locals())
        else:
            form_obj = BaseModeForm(request.POST, instance=edit_obj)
            if form_obj.is_valid():
                form_obj.save()
                return redirect(self.get_list_url())
            else:
                return render(request, 'stark/edit_view.html', locals())

    def delete_view(self, request, id):
        if request.method == 'POST':
            self.model.objects.filter(pk=id).delete()
            return redirect(self.get_list_url())
        list_url = self.get_list_url()
        return render(request, 'stark/delete_view.html', locals())

    @property
    def get_urls(self):
        temp = [
            path('', self.list_view, name='{}_{}_list'.format(self.app_label, self.model_name)),
            path('add/', self.add_view, name='{}_{}_add'.format(self.app_label, self.model_name)),
            re_path('(\d+)/edit/', self.edit_view, name='{}_{}_edit'.format(self.app_label, self.model_name)),
            re_path('(\d+)/delete/', self.delete_view, name='{}_{}_delete'.format(self.app_label, self.model_name)),
        ]
        return temp, None, None


class StarkSite:
    def __init__(self):
        self._registry = {}

    def register(self, model, admin_class=None, **options):
        admin_class = admin_class or ModelStark
        self._registry[model] = admin_class(model)

    def get_urls(self):
        temp = []
        for model, config_obj in self._registry.items():
            model_name = model._meta.model_name
            app_lable = model._meta.app_label
            temp.append(
                path('{}/{}/'.format(app_lable, model_name), config_obj.get_urls)
            )
        return temp

    @property
    def urls(self):
        return self.get_urls(), None, None


site = StarkSite()
