from ...core.apirouter import MisagoApiRouter
from ..api import CategoryViewSet

router = MisagoApiRouter()
router.register(r"categories", CategoryViewSet, basename="category")
urlpatterns = router.urls
