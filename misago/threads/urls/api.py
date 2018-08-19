from misago.core.apirouter import MisagoApiRouter
from misago.threads.api.attachments import AttachmentViewSet
from misago.threads.api.threadpoll import ThreadPollViewSet
from misago.threads.api.threadposts import PrivateThreadPostsViewSet, ThreadPostsViewSet
from misago.threads.api.threads import PrivateThreadViewSet, ThreadViewSet


router = MisagoApiRouter()

router.register(r'attachments', AttachmentViewSet, base_name='attachment')

router.register(r'threads', ThreadViewSet, base_name='thread')
router.register(
    r'threads/(?P<thread_pk>[^/.]+)/posts', ThreadPostsViewSet, base_name='thread-post'
)
router.register(r'threads/(?P<thread_pk>[^/.]+)/poll', ThreadPollViewSet, base_name='thread-poll')

router.register(r'private-threads', PrivateThreadViewSet, base_name='private-thread')
router.register(
    r'private-threads/(?P<thread_pk>[^/.]+)/posts',
    PrivateThreadPostsViewSet,
    base_name='private-thread-post'
)

urlpatterns = router.urls
