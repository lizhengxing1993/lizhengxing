from haystack import indexes
from books.models import Books

#指定对于某个类的某些数据建立索引，　一般类名：模型类名+Index
class BooksIndex(indexes.SearchIndex, indexes.Indexable):
	#指定根据那些字段建立索引
	text = indexes.CharField(document=True, use_template=True)

	def get_model(self):
		return Books

	def index_queryset(self, using=None):
		return self.get_model().objects.all()

