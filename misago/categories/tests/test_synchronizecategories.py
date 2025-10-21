from io import StringIO

from django.core import management

from ..management.commands import synchronizecategories


def call_command():
    command = synchronizecategories.Command()

    out = StringIO()
    management.call_command(command, stdout=out)
    return tuple(l.strip() for l in out.getvalue().strip().splitlines())


def test_synchronizecategories_command_synchronizes_empty_category(default_category):
    command_output = call_command()
    assert command_output[-1].startswith("Synchronized 3 categories")

    default_category.refresh_from_db()

    assert default_category.threads == 0
    assert default_category.posts == 0
    assert default_category.unapproved_threads == 0
    assert default_category.unapproved_posts == 0
    assert default_category.last_posted_at is None
    assert default_category.last_thread is None
    assert default_category.last_thread_title is None
    assert default_category.last_thread_slug is None
    assert default_category.last_poster is None
    assert default_category.last_poster_name is None
    assert default_category.last_poster_slug is None


def test_synchronizecategories_command_synchronizes_category_with_threads(
    thread_factory, thread_reply_factory, default_category
):
    threads = [thread_factory(default_category) for _ in range(10)]
    for thread in threads:
        for _ in range(5):
            thread_reply_factory(thread)

    command_output = call_command()
    assert command_output[-1].startswith("Synchronized 3 categories")

    default_category.refresh_from_db()

    last_thread = threads[-1]

    assert default_category.threads == 10
    assert default_category.posts == 60
    assert default_category.unapproved_threads == 0
    assert default_category.unapproved_posts == 0
    assert default_category.last_posted_at == last_thread.last_posted_at
    assert default_category.last_thread == last_thread
    assert default_category.last_thread_title == last_thread.title
    assert default_category.last_thread_slug == last_thread.slug
    assert default_category.last_poster == last_thread.last_poster
    assert default_category.last_poster_name == last_thread.last_poster_name
    assert default_category.last_poster_slug == last_thread.last_poster_slug
