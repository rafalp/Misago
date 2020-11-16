from django.conf.urls import url

from ...conf import settings
from ...core.views import home_redirect

from ..views import categories

if settings.MISAGO_THREADS_ON_INDEX:
    URL_PATH = r"^categories/$"
else:
    URL_PATH = r"^$"

urlpatterns = [
    url(URL_PATH, categories, name="categories"),
    # fallback for after we changed index setting
    url(r"^categories/$", home_redirect),
]
