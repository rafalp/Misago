from django.urls import path

from .views.selectcategory import SelectCategoryView
from .views.start import StartPrivateThreadView, StartThreadView


urlpatterns = [
    path(
        "start-thread/",
        SelectCategoryView.as_view(),
        name="start-thread",
    ),
    path(
        "c/<slug:slug>/<int:id>/start-thread/",
        StartThreadView.as_view(),
        name="start-thread",
    ),
    path(
        "private/start-thread/",
        StartPrivateThreadView.as_view(),
        name="start-private-thread",
    ),
]
