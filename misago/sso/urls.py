from django.conf.urls import url, include
from .client import client

urlpatterns = [url(r"^client/", include(client.get_urls()))]
