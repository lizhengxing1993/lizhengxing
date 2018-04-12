"""bookstore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from users import views

urlpatterns = [
    url(r'^register/$', views.register, name='register'), # 用户注册
    url(r'^register_handle/$', views.register_handle, name='register_handle'), # 用户注册处理
    url(r'^login/$', views.login, name='login'), # 显示登陆页面
    url(r'^login_check/$', views.login_check, name='login_check'), # 用户登录校验
    url(r'^logout/$', views.logout, name='logout'), # 退出用户登录
    url(r'^$', views.user, name='user'), # 用户中心-信息页
    url(r'^address/$', views.address, name='address'), # 用户中心-地址页
    url(r'^order/$', views.order, name='order'), #用户中心－订单页
    url(r'^verifycode/$', views.verifycode, name='verifycode'), #验证码功能
    url(r'^active/(?P<token>).*/$', views.register_active, name='active'),#用户激活


]
