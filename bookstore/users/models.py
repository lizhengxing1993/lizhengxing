from django.db import models
from db.base_model import BaseModel
from utils.get_hash import get_hash

class PassportManageer(models.Manager):
	def add_one_passport(self, username, password, email):
		# '''添加一个账户信息'''
		passport = self.create(username=username, password=get_hash(password), email=email)
		# 	返回passport
		return passport

	def get_one_passport(self, username, password):
		# 根据账号密码查找信息
		try:
			passport = self.get(username=username, password=get_hash(password))
		except self.model.DoesNotExist:
			passport = None
		return passport
	def check_passport(self, username):
		try:
			passport = self.get(username=username)
		except self.model.DoesNotExist:
			passport = None
		return passport



# Create your models here.
class Passport(BaseModel):
	# 	用户类模型
	username = models.CharField(max_length=20, verbose_name='用户名称')
	password = models.CharField(max_length=40, verbose_name='用户密码')
	email = models.EmailField(verbose_name='用户邮箱')

	# 	用户列表管理器
	objects = PassportManageer()

	class Meta:
		db_table = 's_user_account'

class AddressManager(models.Manager):
	'''地址模型类－－管理'''
	def get_default_address(self, passport_id):
		'''查询指定用户的默认收货地址'''
		try:
			addr = self.get(passport_id, is_default=True)
		except self.model.DoesNotExist:
			#没有收货地址
			addr = None
		return addr
	def add_one_address(self, passport_id, recipient_name, recipient_addr, zip_code,recipient_phone):
		'''添加收货地址'''
		#判断用户是否有默认收货地址
		addr = self.get_default_address(passport_id=passport_id)

		if addr:
			#有默认地址
			is_default = False
		else:
			#没有默认地址
			is_default = True

		#添加一个地址
		addr = self.create(passport_id=passport_id,
						   recipient_name=recipient_name,
						   recipient_addr=recipient_addr,
						   zip_code=zip_code,
						   recipient_phone=recipient_phone,
						   is_default=is_default
						   )
		return addr

class Address(BaseModel):
	'''地址模型类'''
	recioient_name = models.CharField(max_length=20, verbose_name='收件人')
	recioient_addr = models.CharField(max_length=256, verbose_name='收件人地址')
	zip_code = models.CharField(max_length=6, verbose_name='邮政编码')
	recipient_phone = models.CharField(max_length=11, verbose_name='联系电话')
	is_default = models.BooleanField(default=False, verbose_name='是否默认')
	passport = models.ForeignKey('Passport', verbose_name='账户')

	objects = AddressManager()

	class Meta:
		db_table = 's_user_address'
