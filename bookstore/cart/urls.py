from django.conf.urls import url
from cart import views
urlpatterns = [
	url(r'^add/$', views.cart_add, name='add'), #添加商品到购物车
	url(r'^count/$', views.cart_count, name='count'), #获取购物车中的商品数量
	url(r'^$', views.cart_show, name='show'), #显示购物车页面
	url(r'^del/$', views.cart_del, name='delete'), #购物车商品记录删除

]