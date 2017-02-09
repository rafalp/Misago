from misago.categories.api import CategoryViewSet
from misago.core.apirouter import MisagoApiRouter


router = MisagoApiRouter()
router.register(r'categories', CategoryViewSet, base_name='category')
urlpatterns = router.urls
