from django.conf.urls import url

from ..views.categorieslist import api


urlpatterns = [
    url(r'^categories/$', api, name='categories'),
]
