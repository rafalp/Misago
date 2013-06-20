from haystack import indexes
from misago.models import Post

class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    forum = indexes.IntegerField(model_attr='forum_id')
    thread = indexes.CharField(model_attr='thread')
    user = indexes.CharField(model_attr='user_name')
    date = indexes.DateTimeField(model_attr='date')

    def get_model(self):
        return Post

    def prepare_thread(self, obj):
        return obj.thread.name

    def get_updated_field(self):
        return 'current_date'

    def should_update(self, instance, **kwargs):
        if (instance.deleted or instance.moderated
                or instance.thread.deletedor or instance.thread.moderated):
            self.remove_object(instance, **kwargs)
            return False
        return True

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
