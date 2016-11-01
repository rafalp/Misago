from misago.core.apirouter import MisagoApiRouter

from ..api.attachments import AttachmentViewSet
from ..api.threadposts import ThreadPostsViewSet
from ..api.threads import ThreadViewSet
from ..api.threadpoll import ThreadPollViewSet


router = MisagoApiRouter()
router.register(r'attachments', AttachmentViewSet, base_name='attachment')
router.register(r'threads', ThreadViewSet, base_name='thread')
router.register(r'threads/(?P<thread_pk>[^/.]+)/posts', ThreadPostsViewSet, base_name='thread-post')
router.register(r'threads/(?P<thread_pk>[^/.]+)/poll', ThreadPollViewSet, base_name='thread-poll')
urlpatterns = router.urls
