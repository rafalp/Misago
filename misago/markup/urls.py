from django.conf.urls import url

from .api import parse_markup


urlpatterns = [url(r'^parse-markup/$', parse_markup, name='parse-markup')]
