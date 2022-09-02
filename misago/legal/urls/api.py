from django.urls import path

from ..api import submit_agreement

urlpatterns = [
    path("submit-agreement/<int:pk>/", submit_agreement, name="submit-agreement")
]
