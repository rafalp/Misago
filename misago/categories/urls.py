from django.urls import path

from . import views

urlpatterns = [
    path("categories/", views.index, name="categories", kwargs={"is_index": False}),
]
