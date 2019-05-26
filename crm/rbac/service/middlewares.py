# __author: iamironman
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect
import re


class PermissionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        current_path = request.path
        for reg in ['/login/', '/reg/', '/admin/*', '/logout/', '/msg/']:
            permission_url = '^{}$'.format(reg)
            ret = re.search(permission_url, current_path)
            if ret:
                return None
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('/login/')
        if user_id == 4:
            return None
        permission_list = request.session.get('permission_list')
        for permission in permission_list:
            permission_url = permission.get('url')
            permission_url = '^{}$'.format(permission_url)
            ret = re.search(permission_url, current_path)
            if ret:
                return None
        return HttpResponse(
            '<center><h2>您没有权限执行该操作，请联系管理员。邮箱：875674794@qq.com</h2>'
            '<br><h2>You do not have permission to perform this operation, '
            'please contact your administrator.email:875674794@qq.com</h2></center>'
	    '<script>setTimeout(function () {window.history.back()}, 3000)</script>')
