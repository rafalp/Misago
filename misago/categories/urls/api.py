from django.conf.urls import url

from misago.categories.views import api


urlpatterns = [
    url(r'^categories/$', api, name='categories'),
]
