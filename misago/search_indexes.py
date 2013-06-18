from haystack import indexes
from misago.models import Post

class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    forum = indexes.CharField(model_attr='forum')
    thread = indexes.CharField(model_attr='thread')
    user = indexes.CharField(model_attr='user_name')
    date = indexes.DateTimeField(model_attr='date')

    def get_model(self):
        return Post

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
