from django.db import models


# Create your models here.


class Book(models.Model):
    title = models.CharField(max_length=32, verbose_name='名称')
    price = models.IntegerField(verbose_name='价格')
    publish = models.ForeignKey('Publish', on_delete=models.CASCADE, verbose_name='出版社')
    authors = models.ManyToManyField('Author')
    state = models.IntegerField(choices=[(1, '已出版'), (2, '未出版')], default=1, verbose_name="出版状态")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '书籍'


class Publish(models.Model):
    name = models.CharField(max_length=32, verbose_name='名称')
    city = models.CharField(max_length=64, verbose_name="城市", null=True)
    email = models.EmailField(verbose_name="邮箱", null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '出版社'


class Author(models.Model):
    name = models.CharField(max_length=32, verbose_name="姓名")
    age = models.IntegerField(verbose_name="年龄")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "作者"
