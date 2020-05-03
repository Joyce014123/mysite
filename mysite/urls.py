"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from login import views as login_views     # 使用根目录下下的url（路由）
from django.conf.urls import include   # 在根目录下添加二级路由


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/', login_views.index),  # 将路由发给login目录下的index
    url(r'^login/', login_views.login),
    url(r'^register/', login_views.register),
    url(r'^logout/', login_views.logout),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^confirm/$', login_views.user_confirm),
]
