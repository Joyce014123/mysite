from django.db import models

# Create your models here.

class User(models.Model):

    gender = (
        ('male', '男'),
        ('female', '女'),
    )

    name = models.CharField(max_length=128, unique=True, verbose_name='用户名')
    password = models.CharField(max_length=256, verbose_name='密码')
    email = models.EmailField(unique=True, verbose_name='邮箱')
    sex = models.CharField(choices=gender, max_length=32, default='男', verbose_name='性别')
    c_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    has_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    class Meta:
        ordering = ['-c_time']    # 根据注册时间进行排序，负号代表谁后注册谁先排序
        verbose_name = '用户'    # 更直观的展示名
        verbose_name_plural = '用户'


class ConfirmString(models.Model):
    code = models.CharField(max_length=256, verbose_name='确认码')
    user = models.OneToOneField('user', verbose_name='关联的用户')
    c_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return self.user.name + ': '+self.code

    class Meta:
        ordering = ['-c_time']
        verbose_name = '确认码'
        verbose_name_plural = '确认码'
















