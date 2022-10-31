from django.urls import path

from . import views


urlpatterns = [
    path("login/<str:backend>/", views.auth, name="social-begin"),
    path("complete/<str:backend>/", views.complete, name="social-complete"),
]
