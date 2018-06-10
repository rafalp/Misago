from django.conf.urls import url

from . import views

urlpatterns = [
   url(r'^$', views.legals_active, name='legal'),
   url(r'^(?P<title>\S+)/$', views.legal_title, name='legal_title'),
]