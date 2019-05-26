from django.db import models


# Create your models here.


class UserInfo(models.Model):
    name = models.CharField(max_length=32, verbose_name='用户名')
    pwd = models.CharField(max_length=32, verbose_name='密码')
    roles = models.ManyToManyField('Role')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '用户信息'


class Role(models.Model):
    title = models.CharField(max_length=32, verbose_name='名称')
    permissions = models.ManyToManyField('Permission', verbose_name='权限')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '角色'


class Permission(models.Model):
    url = models.CharField(max_length=128, blank=True, verbose_name='路径')
    title = models.CharField(max_length=32, verbose_name='名称')
    type = models.CharField(max_length=32, choices=[('menu', '菜单权限'), ('menuLink', '菜单链接权限'), ('button', '按钮权限')],
                            default='button', verbose_name='类型')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, verbose_name='父级')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '权限'
