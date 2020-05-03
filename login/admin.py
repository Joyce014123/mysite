from django.contrib import admin

# Register your models here.    # 后台，创建测试用例，观察模型效果

from . import models   # 从login目录下导入models文件

admin.site.register(models.User)      # 注册

# 用命令创建超级用户，启用后台管理员，和models中的user是两码事
admin.site.register(models.ConfirmString)

