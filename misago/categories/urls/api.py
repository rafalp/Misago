from django.conf.urls import url

from ..views import api


urlpatterns = [
    url(r'^categories/$', api, name='categories'),
]
