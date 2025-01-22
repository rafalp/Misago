import pytest
from django.urls import reverse

from ...attachments.models import Attachment
from ...test import assert_contains

filetypes_url = reverse("misago:admin:attachments:filetypes:index")


def test_attachments_filetypes_link_is_registered_in_admin_nav(admin_client):
    response = admin_client.get(
        reverse("misago:admin:attachments:index") + "?redirected=1"
    )
    assert_contains(response, filetypes_url)


def test_attachments_filetypes_list_renders_filetypes(admin_client):
    response = admin_client.get(filetypes_url)
    assert_contains(response, ".mp4")
    assert_contains(response, "video/mp4")
