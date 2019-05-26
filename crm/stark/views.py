from django.shortcuts import render, redirect, HttpResponse
from rbac.models import UserInfo, Role


# Create your views here.
def reg(request):
    if request.method == 'GET':
        return render(request, 'stark/reg.html')
    else:
        res = {'msg': ''}
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        user_exist = UserInfo.objects.filter(name=user).first()
        if not user_exist:
            role_obj = Role.objects.get(id=3)
            user_obj = role_obj.userinfo_set.create(name=user, pwd=pwd)
            request.session['user_id'] = user_obj.pk
            permissions = user_obj.roles.all().values('permissions__url',
                                                      'permissions__title',
                                                      'permissions__pk',
                                                      'permissions__type',
                                                      'permissions__parent_id',
                                                      ).distinct()
            permission_list = []
            for permission in permissions:
                permission_list.append({
                    'url': permission['permissions__url'],
                    'title': permission['permissions__title'],
                    'pk': permission['permissions__pk'],
                    'type': permission['permissions__type'],
                    'pid': permission['permissions__parent_id'],
                })
            request.session['permission_list'] = permission_list
            request.session['user'] = user_obj.name
            return redirect('/stark/app01/book/')
        else:
            res['msg'] = '用户名已存在，请重新注册'
        return render(request, 'stark/reg.html', {'res': res})


def login(request):
    if request.method == 'GET':
        return render(request, 'stark/login.html')
    else:
        res = {'msg': ''}
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        user_obj = UserInfo.objects.filter(name=user, pwd=pwd).first()
        if user_obj:
            request.session['user_id'] = user_obj.pk
            permissions = user_obj.roles.all().values('permissions__url',
                                                      'permissions__title',
                                                      'permissions__pk',
                                                      'permissions__type',
                                                      'permissions__parent_id',
                                                      ).distinct()
            permission_list = []
            for permission in permissions:
                permission_list.append({
                    'url': permission['permissions__url'],
                    'title': permission['permissions__title'],
                    'pk': permission['permissions__pk'],
                    'type': permission['permissions__type'],
                    'pid': permission['permissions__parent_id'],
                })
            request.session['permission_list'] = permission_list
            request.session['user'] = user_obj.name
            return redirect('/stark/app01/book/')
        else:
            res['msg'] = '用户名或密码错误'
        return render(request, 'stark/login.html', {'res': res})


def logout(request):
    request.session.flush()
    return redirect('/login/')


def msg(request):
    return HttpResponse('<center><h3>程序猿很忙滴，这个功能暂时不做了。</h3></cenr>'
			'<script>setTimeout(function () {window.history.back()}, 2000)</script>')
