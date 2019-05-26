# __author: iamironman
from stark.service.sites import site, ModelStark
from .models import *
from django.forms import ModelForm


class BookModelForm(ModelForm):
    class Meta:
        model = Book
        fields = "__all__"
        error_messages = {
            "title": {"required": " 该字段不能为空!"},
            "price": {"required": " 该字段不能为空!"},
            "publish": {"required": " 该字段不能为空!"},
            "authors": {"required": " 该字段不能为空!"},
            "state": {"required": " 该字段不能为空!"},
        }


class BookConfig(ModelStark):
    def show_authors(self, obj=None, header=False):
        if header:
            return "作者信息"
        return " ".join([author.name for author in obj.authors.all()])

    def patch_init(self, request, queryset):
        queryset.update(price=0)

    patch_init.desc = "价格初始化"
    actions = [patch_init, ]
    list_display = ["title", "price", "publish", "state", show_authors]
    search_fields = ["title", "price"]
    # per_page_num = 3
    list_display_links = ["title", "price", "publish", "state", ]
    model_form_class = BookModelForm
    list_filter = ["publish", "authors", "state"]


class PublishModelForm(ModelForm):
    class Meta:
        model = Publish
        fields = "__all__"
        error_messages = {
            "name": {"required": " 该字段不能为空!"},
            "city": {"required": " 该字段不能为空!"},
            "email": {"required": " 该字段不能为空!"},
        }


class PublishConfig(ModelStark):
    list_display = ["name", "city", "email"]
    search_fields = ["name", "city", "email"]
    list_display_links = ["name", "city", "email"]
    model_form_class = PublishModelForm


class AuthorModelForm(ModelForm):
    class Meta:
        model = Author
        fields = "__all__"
        error_messages = {
            "name": {"required": " 该字段不能为空!"},
            "age": {"required": " 该字段不能为空!"},
        }


class AuthorConfig(ModelStark):
    list_display = ["name", "age"]
    search_fields = ["name", "age"]
    list_display_links = ["name", "age"]
    model_form_class = AuthorModelForm


site.register(Book, BookConfig)
site.register(Publish, PublishConfig)
site.register(Author, AuthorConfig)
