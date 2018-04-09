from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
import re
from users.models import Passport, Address
from django.http import JsonResponse
from utils.decorators import login_required
from books.models import Books
from django_redis import get_redis_connection
from utils.get_hash import get_hash

# Create your views here.
def register(request):
	'''显示用户注册页面'''
	return render(request, 'users/register.html')

def register_handle(request):
	'''进行用户注册处理'''
	# 接收数据
	username = request.POST.get('user_name')
	password = request.POST.get('pwd')
	email = request.POST.get('email')

	# 进行数据校验
	if not all([username, password, email]):
		# 有数据为空
		return render(request, 'users/register.html', {'errmsg': '参数不能为空!'})

	# 判断邮箱是否合法
	if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
		# 邮箱不合法
		return render(request, 'users/register.html', {'errmsg': '邮箱不合法!'})
	try:
		p = Passport.objects.check_passport(username=username)
	except Exception as e:
		print('e: ', e)
	print('p: ', p)
	if p:
		return render(request, 'users/register.html', {'errmsg': '用户名已存在！'})

	# 进行业务处理:注册，向账户系统中添加账户
	# Passport.objects.create(username=username, password=password, email=email)
	passport = Passport.objects.add_one_passport(username=username, password=password, email=email)

	# 注册完，还是返回注册页。
	return redirect(reverse('books:index'))

def login(request):
	'''显示登录页面'''
	username = ''
	checked = ''

	context = {
		'username': username,
		'checked': checked,
	}

	return render(request, 'users/login.html', context)

# /user/logout
def logout(request):
	'''用户退出登录'''
	# 清空用户的session信息
	request.session.flush()
	# 跳转到首页
	return redirect(reverse('books:index'))

def login_check(request):
	'''进行用户登录校验'''
	# 1.获取数据
	username = request.POST.get('username')
	password = request.POST.get('password')
	remember = request.POST.get('remember')
	# vcode = request.POST.get('verifycode')

	# 2.数据校验
	if not all([username, password, remember]):
		# 有数据为空
		return JsonResponse({'res': 2})

	# if verifycode.upper() != request.session['verifycode']:
	# 	return JsonResponse({'res': 2})

	# 3.进行处理:根据用户名和密码查找账户信息
	passport = Passport.objects.get_one_passport(username=username, password=password)
	print('passport', passport)
	if passport:
		# 用户名密码正确
		# 获取session中的url_path

		next_url = request.session.get('url_path', reverse('books:index')) #/user
		jres = JsonResponse({'res': 1, 'next_url': next_url})

		# 判断是否需要记住用户名
		if remember == 'true':
			# 记住用户名
			jres.set_cookie('username', username, max_age=7*24*3600)
		else:
			# 不要记住用户名
			jres.delete_cookie('username')

		# 记住用户的登录状态
		request.session['islogin'] = True
		request.session['username'] = username
		request.session['passport_id'] = passport.id
		return jres
	else:
		# 用户名或密码错误
		return JsonResponse({'res': 0})

@login_required
def user(request):
	'''用户中心-信息页'''
	passport_id = request.session.get('passport_id')
	# 获取用户的基本信息
	addr = Address.objects.get_default_address(passport_id=passport_id)

	# 获取用户的最近浏览信息
	con = get_redis_connection('default')
	key = 'history_%d' % passport_id
	# 取出用户最近浏览的5个商品的id
	history_li = con.lrange(key, 0, 4)
	# history_li = [21,20,11]
	# print(history_li)
	# 查询数据库,获取用户最近浏览的商品信息
	# books_li = Books.objects.filter(id__in=history_li)
	books_li = []
	for id in history_li:
		books = Books.objects.get_books_by_id(books_id=id)
		books_li.append(books)

	return render(request, 'users/user_center_info.html', {'addr': addr,
														   'page': 'user',
														   'books_li': books_li})

@login_required
def address(request):
	'''用户中心-地址页'''
	# 获取登录用户的id
	passport_id = request.session.get('passport_id')

	if request.method == 'GET':
		# 显示地址页面
		# 查询用户的默认地址
		addr = Address.objects.get_default_address(passport_id=passport_id)
		return render(request, 'users/user_center_site.html', {'addr': addr, 'page': 'address'})
	else:
		# 添加收货地址
		# 1.接收数据
		recipient_name = request.POST.get('username')
		recipient_addr = request.POST.get('addr')
		zip_code = request.POST.get('zip_code')
		recipient_phone = request.POST.get('phone')

		# 2.进行校验
		if not all([recipient_name, recipient_addr, zip_code, recipient_phone]):
			return render(request, 'users/user_center_site.html', {'errmsg': '参数不必为空!'})

		# 3.添加收货地址
		Address.objects.add_one_address(passport_id=passport_id,
										recipient_name=recipient_name,
										recipient_addr=recipient_addr,
										zip_code=zip_code,
										recipient_phone=recipient_phone)

		# 4.返回应答
		return redirect(reverse('user:address'))