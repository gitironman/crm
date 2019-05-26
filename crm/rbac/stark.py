# __author: iamironman
from stark.service.sites import site, ModelStark
from .models import *


class UserInfoConfig(ModelStark):
    def show_roles(self, obj=None, header=False):
        if header:
            return "角色信息"
        return " ".join([role.title for role in obj.roles.all()])

    list_display = ['id', 'name', show_roles]
    search_fields = ["id", "name"]
    list_display_links = ["id", "name"]
    list_filter = ["roles"]

    def patch_delete(self, request, queryset):
        pass

    patch_delete.desc = None
    actions = [patch_delete, ]


class RoleConfig(ModelStark):
    def show_permissions(self, obj=None, header=False):
        if header:
            return "角色信息"
        return " ".join([permission.title for permission in obj.permissions.all()])

    list_display = ['title', show_permissions]
    search_fields = ["title"]
    list_display_links = ["title"]
    list_filter = ["permissions"]

    def patch_delete(self, request, queryset):
        pass

    patch_delete.desc = None
    actions = [patch_delete, ]


class PermissionConfig(ModelStark):
    list_display = ['id', 'title', 'url', 'type', 'parent']
    per_page_num = 20
    search_fields = ['id', 'title', 'url', 'type']
    list_display_links = ['id', 'title', 'url']
    list_filter = ['parent']

    def patch_delete(self, request, queryset):
        pass

    patch_delete.desc = None
    actions = [patch_delete, ]


site.register(UserInfo, UserInfoConfig)
site.register(Role, RoleConfig)
site.register(Permission, PermissionConfig)
