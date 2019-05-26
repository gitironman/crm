# __author: iamironman
from django import template

register = template.Library()


@register.simple_tag
def my_date(date):
    s = '{}年{}月{}日'.format(date.year, date.month, date.day)
    return s


@register.simple_tag
def get_menu(request):
    permission_list = request.session.get('permission_list')
    menu_permissions = []
    for permission in permission_list:
        if permission.get('type') == 'button':
            continue
        menu_permissions.append(permission)
    return menu_permissions


@register.inclusion_tag('rbac/menu.html')
def get_menu_style(request):
    permission_list = request.session.get('permission_list')
    permissions_dict = {}
    for permission in permission_list:
        if permission.get('type') == 'button':
            continue
        pk = permission.get('pk')
        temp = {}
        temp['text'] = permission.get('title') or ''
        temp['href'] = permission.get('url') or ''
        temp['pk'] = permission.get('pk') or ''
        temp['pid'] = permission.get('pid') or ''
        permissions_dict[pk] = temp
    permission_tree = []
    for permission_pk, permission_dict in permissions_dict.items():
        pid = permission_dict.get('pid')
        if pid:
            if not permissions_dict[pid].get('nodes'):
                permissions_dict[pid]['nodes'] = [permission_dict]
            else:
                permissions_dict[pid]['nodes'].append(permission_dict)
        else:
            permission_tree.append(permission_dict)
        if permission_dict.get('href') == request.path:
            permission_dict['backColor'] = '#ccc'
            permission_dict['color'] = 'white'
            while pid:
                permissions_dict[pid]['state'] = {'expanded': True}
                pid = permissions_dict[pid]['pid']
    import json
    return {'permission_tree': json.dumps(permission_tree)}
