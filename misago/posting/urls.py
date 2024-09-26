from django.urls import path

from .views.reply import ReplyPrivateThreadView, ReplyThreadView
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
    path(
        "t/<slug:slug>/<int:id>/reply/",
        ReplyThreadView.as_view(),
        name="thread-reply",
    ),
    path(
        "p/<slug:slug>/<int:id>/reply/",
        ReplyPrivateThreadView.as_view(),
        name="private-thread-reply",
    ),
]
