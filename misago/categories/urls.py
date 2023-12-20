from django.urls import path

from ..conf import settings
from ..core.views import home_redirect

from . import views

if settings.MISAGO_THREADS_ON_INDEX:
    URL_PATH = "categories/"
else:
    URL_PATH = ""

urlpatterns = [
    path(URL_PATH, views.index, name="categories"),
    # fallback for after we changed index setting
    path("categories/", home_redirect),
]
