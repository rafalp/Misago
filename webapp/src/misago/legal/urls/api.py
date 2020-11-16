from django.conf.urls import url

from ..api import submit_agreement

urlpatterns = [
    url(r"^submit-agreement/(?P<pk>\d+)/$", submit_agreement, name="submit-agreement")
]
