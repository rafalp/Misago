from misago.core.apirouter import MisagoApiRouter
from misago.threads.api.threads import ThreadViewSet


router = MisagoApiRouter()
router.register(r'threads', ThreadViewSet, base_name='thread')
urlpatterns = router.urls