from django.shortcuts import render
from django.http import JsonResponse
from django_redis import get_redis_connection
from books.models import Books
from utils.decorators import login_required

# 前端发过来的数据： 商品id 商品数目　books_id books_count
def cart_add(request):
	'''给购物车添加数据'''
	# 判断用户是否登录
	if not request.session.has_key('islogin'):
		return JsonResponse({'fes': 0, 'reemsg': '请先登录'})

	# 获取书的id
	books_id = request.POST.get('books_id')
	# 获取书的数量
	books_count = request.POST.get('books_count')

	# 进行数据校验
	if not all([books_id, books_count]):
		return JsonResponse({'res': 1, 'errmsg': '数据不完整'})
	# 根据id获取到书的信息
	books = Books.objects.get_books_by_id(books_id=books_id)

	if books is None:
		'''商品不存在'''
		return JsonResponse({'res': 2, 'errmsg': '商品不存在'})

	try:
		count = int(books_count)
	except Exception as e:
		# 商品数量不合法
		return JsonResponse({'res': 3, 'errmsg': '商品数量必须为数字'})

	# 添加商品到购物车
	# 每个用户的购物车记录用一条hash数据保存，格式：cart_用户id:商品id　商品数量
	conn = get_redis_connection('default')
	# 获取每个客户的购物车id
	cart_key = 'cart_%d' % request.session.get('passport_id')

	res = conn.hget(cart_key, books_id)

	if res is None:
		'''如果购物车中没有添加过该商品，则添加数据'''
		res = count
	else:
		'''如果用户的购物车中已经添加了该商品，则累计商品数目'''
		res = int(res) + count

	if res > books.stock:
		# 库存不足
		return JsonResponse({'res': 4, 'errmsg': '商品库存不足'})
	else:
		conn.hset(cart_key, books_id, res)

	# 返回结果
	return JsonResponse({'res': 5})

def cart_count(request):
	'''获取购物车中商品的数量'''
	#判断用户是否登录
	if not request.session.has_key('islogin'):
		return JsonResponse({'res': 0})
	#计算用户购物车商品的数量
	conn = get_redis_connection('default')#改为从redis中获取数据
	cart_key = 'cart_%d' % request.session.get('passport_id')
	#res = conn.hlen(cart_key)显示商品的数量
	res = 0
	res_list = conn.hvals(cart_key)

	for i in res_list:
		res += int(i)

	#返回结果
	return JsonResponse({'res': res})


@login_required
def cart_show(request):
	'''显示用户购物车页面'''
	passport_id = request.session.get('passport_id')
	# 获取购物车记录
	conn = get_redis_connection('default')  #  获取redis数据库
	cart_key = 'cart_%d' % passport_id  #  拼接key 用户的
	res_dict = conn.hgetall(cart_key)


	books_li = []
	# 存放商品数量
	total_count = 0
	# 保存总价
	total_price = 0

	# 遍历res_dict获取商品的数据
	for id, count in res_dict.items():
		# 根据id获取商品数据
		books = Books.objects.get_books_by_id(books_id=id)
		# 保存商品的数目
		books.count = count
		# 保存商品的小计
		books.amount = int(count) * books.price

		books_li.append(books)


		total_count += int(count)
		total_price += int(count) * books.price

	# 定义模板上下文
	context = {
		'books_li': books_li,
		'total_price': total_price,
		'total_count': total_count
	}
	return render(request, 'cart/cart.html', context)

def cart_del(request):
	'''删除购物车商品'''
	#先判断是否登录
	if not request.session.hax_key('islogin'):
		return JsonResponse({'res': 0, 'errmsg': '请先登录'})

	#接收数据
	books_id = request.POST.get('book_id')

	# 检验商品是否存放
	if not all([books_id]):
		return JsonResponse({'res': 1, 'errmsg': '数据不完整'})

	books = Books.objects.get_books_by_id(books_id)
	if books is None:
		return JsonResponse({'res': 2, 'errmsg': '商品不存在'})
	# 删除购物车商品信息
	conn = get_redis_connection('default')
	cart_key = 'cart_%d' % request.session.get('passport_id')
	conn.hdel(cart_key, books_id)
	# 返回信息
	return JsonResponse({'res': 3})
