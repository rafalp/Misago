from ...core.apirouter import MisagoApiRouter
from ..api.attachments import AttachmentViewSet
from ..api.threadpoll import ThreadPollViewSet
from ..api.threadposts import PrivateThreadPostsViewSet, ThreadPostsViewSet
from ..api.threads import PrivateThreadViewSet, ThreadViewSet

router = MisagoApiRouter()

router.register(r"attachments", AttachmentViewSet, basename="attachment")

router.register(r"threads", ThreadViewSet, basename="thread")
router.register(
    r"threads/(?P<thread_pk>[^/.]+)/posts", ThreadPostsViewSet, basename="thread-post"
)
router.register(
    r"threads/(?P<thread_pk>[^/.]+)/poll", ThreadPollViewSet, basename="thread-poll"
)

router.register(r"private-threads", PrivateThreadViewSet, basename="private-thread")
router.register(
    r"private-threads/(?P<thread_pk>[^/.]+)/posts",
    PrivateThreadPostsViewSet,
    basename="private-thread-post",
)

urlpatterns = router.urls
