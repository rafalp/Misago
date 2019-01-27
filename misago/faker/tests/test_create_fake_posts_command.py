from io import StringIO

from django.core.management import call_command

from ...threads.models import Post
from ..management.commands import createfakeposts
from ..threads import get_fake_thread


def test_management_command_creates_fake_threads(fake, default_category):
    thread = get_fake_thread(fake, default_category)
    call_command(createfakeposts.Command(), stdout=StringIO())
    assert Post.objects.exclude(pk=thread.first_post.pk).exists()
