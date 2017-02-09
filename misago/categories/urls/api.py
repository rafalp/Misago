from misago.core.apirouter import MisagoApiRouter

from misago.categories.api import CategoryViewSet


router = MisagoApiRouter()
router.register(r'categories', CategoryViewSet, base_name='category')
urlpatterns = router.urls
