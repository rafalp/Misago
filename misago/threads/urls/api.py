from misago.core.apirouter import MisagoApiRouter

from ..api.threadposts import ThreadPostsViewSet
from ..api.threads import ThreadViewSet


router = MisagoApiRouter()
router.register(r'threads', ThreadViewSet, base_name='thread')
router.register(r'threads/(?P<thread_pk>[^/.]+)/posts', ThreadPostsViewSet, base_name='thread-post')
urlpatterns = router.urls
