from django.urls import path

from .api import parse_markup

urlpatterns = [path("parse-markup/", parse_markup, name="parse-markup")]
