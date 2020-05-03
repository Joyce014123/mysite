from django.shortcuts import render
from django.shortcuts import redirect
from . import models
from . import forms
from mysite import settings
import datetime
# Create your views here.

import hashlib

def hash_code(s, salt='mysite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()

def make_confirm_string(user):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.name, now)
    models.ConfirmString.objects.create(code=code, user=user)

    return code

def send_email(email, code):
    from django.core.mail import EmailMultiAlternatives

    subject = '来自www.liujiangblog.com的测试邮件'
    text_content = '''感谢注册问www.liujiangblog.com,这里是刘江的博客和教程站点，专注于python和Django的分享!\
    如果你看到这条消息,说明你的邮箱服务器不提供HTML链接功能，请联系管理员'''

    html_content = '''<p>欢迎访问<a href="http://{}/confirm/?code={}" target=blank>www.liujiangblog.com</a>,\
    这里是刘江的博客和教程站点，专注于python和Django的分享</p>.
    <p>请点击站点链接完成注册确认!</p>
    <p>此链接有效期为{}天!</p>'''.format('127.0.0.1:8000', code, settings.CONFIRM_DAYS)

    msg = EmailMultiAlternatives(subject, text_content,settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

def index(request):
    pass
    return render(request, 'login/index.html')

def login(request):
    if request.session.get('is_login', None):
        return redirect('/index/')
    if request.method == 'POST':
        login_form = forms.UserForm(request.POST)  # login_form是自己取的变量名
        # username = request.POST.get('username', None)
        # password = request.POST.get('password', None)
        message = '所有字段都必须填写!'
        # 验证
        if login_form.is_valid():  #
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
        # ...
            try:
                user = models.User.objects.get(name=username)
            except:
                message = '用户不存在!'
                return render(request, 'login/login.html', locals())
            if not user.has_confirmed:
                message = '该用户还未通过邮件确认!不能登录!'
                return render(request, 'login/login.html', locals())

            # if user.password == password:
            if user.password == hash_code(password):
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                return redirect('/index/')
            else:
                message = '密码错误!'
                return render(request, 'login/login.html', locals())
            # print(username, password)
        else:
            return render(request, 'login/login.html', locals())
        # return redirect('/index/')   # 跳转到首页
    login_form = forms.UserForm()   # 提供空表单

    return render(request, 'login/login.html', locals())

def register(request):
    if request.session.get('is_login', None):
        return redirect('/index/')

    if request.method == "POST":
        register_form = forms.RegisterForm(request.POST)
        message = '请检查填写的内容!'
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:
                message = '两次输入的密码不相同!'
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message = '用户名已经存在,请重新选择!'
                    return render(request, 'login/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:
                    message = '该邮箱已经被注册, 请使用别的邮箱!'
                    return render(request, 'login/register.html', locals())

            new_user = models.User.objects.create()     # 创建新的用户
            new_user.name = username
            # new_user.password = password2
            new_user.password = hash_code(password2)
            new_user.email = email
            new_user.sex = sex
            new_user.save()    # 保存新的用户

            code = make_confirm_string(new_user)  # 生成确认码
            send_email(email, code)

            message = '请前往注册邮箱进行确认!'
            # return redirect('/login/')
            return render(request, 'login/confirm.html', locals())

    register_form = forms.RegisterForm()
    return render(request, 'login/register.html', locals())

def logout(request):
    if not request.session.get('is_login', None):
        return redirect('/index/')
    request.session.flush()
    return redirect('/index/')  # 返回到首页面，已经写死

def user_confirm(request):
    code = request.GET.get('code', None)
    message = ''
    try:
        confirm = models.ConfirmString.objects.get(code=code)
    except:
        message = '无效的请求!'
        return render(request, 'login/confirm.html', locals())

    c_time = confirm.c_time
    now = datetime.datetime.now()

    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = "您的邮件已经过期!请重新注册!"
        return render(request, 'login/confirm.html', locals())
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = '感谢确认,请使用账户登录!'
        return render(request, 'login/confirm.html', locals())




