from datetime import timedelta
from io import StringIO

import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.utils import timezone

from ...categories.models import Category
from ...threads.models import Post, Thread
from ...users.models import Rank
from ..management.commands import createfakehistory
from ..threads import get_fake_thread
from ..users import get_fake_admin_activated_user, get_fake_inactive_user, get_fake_user

User = get_user_model()


@pytest.fixture
def command(db):
    return createfakehistory.Command(stdout=StringIO())


@pytest.fixture
def date():
    return timezone.now()


def test_management_command_has_no_errors(db):
    call_command(createfakehistory.Command(), max_actions=3, stdout=StringIO())


def test_management_command_creates_fake_user(fake, command, date):
    ranks = list(Rank.objects.all())
    command.create_fake_user(fake, date, ranks)
    assert User.objects.exists()


def test_fake_user_join_date_is_overridden_by_command(fake, command, date):
    ranks = list(Rank.objects.all())
    command.create_fake_user(fake, date, ranks)
    user = User.objects.order_by("-pk").last()
    assert user.joined_on == date


def test_fake_user_rank_is_one_from_the_choices(fake, command, date):
    ranks = list(Rank.objects.all())
    command.create_fake_user(fake, date, ranks)
    user = User.objects.order_by("-pk").last()
    assert user.rank in ranks


def test_none_is_returned_for_random_user_if_no_users_exist(command, date):
    user = command.get_random_user(date)
    assert user is None


def test_users_created_after_given_date_are_excluded_from_random_user_pick(
    command, date, other_user
):
    other_user.joined_on = timezone.now()
    other_user.save()

    user = command.get_random_user(date)
    assert user is None


def test_inactive_users_are_excluded_from_random_user_pick(fake, command):
    get_fake_admin_activated_user(fake)
    get_fake_inactive_user(fake)

    user = command.get_random_user(timezone.now())
    assert user is None


def test_random_user_pick_returns_random_user(fake, command):
    valid_choices = [get_fake_user(fake) for _ in range(5)]
    user = command.get_random_user(timezone.now())
    assert user in valid_choices


def test_management_command_creates_fake_thread(fake, command, date):
    categories = list(Category.objects.all_categories())
    command.create_fake_thread(fake, date, categories)
    assert Thread.objects.exists()


def test_fake_thread_start_date_is_overridden_by_command(fake, command, date):
    categories = list(Category.objects.all_categories())
    command.create_fake_thread(fake, date, categories)
    thread = Thread.objects.last()
    assert thread.started_on == date


def test_fake_thread_was_created_in_one_of_valid_categories(fake, command, date):
    categories = list(Category.objects.all_categories())
    command.create_fake_thread(fake, date, categories)
    thread = Thread.objects.last()
    assert thread.category in categories


def test_none_is_returned_for_random_thread_if_no_threads_exist(command, date):
    thread = command.get_random_thread(date)
    assert thread is None


def test_threads_created_after_given_date_are_excluded_from_random_thread_pick(
    fake, command, date, default_category
):
    get_fake_thread(fake, default_category)
    thread = command.get_random_thread(date)
    assert thread is None


def test_random_thread_pick_returns_random_thread(fake, command, default_category):
    valid_choices = [get_fake_thread(fake, default_category) for _ in range(5)]
    thread = command.get_random_thread(timezone.now())
    assert thread in valid_choices


def test_management_command_creates_fake_post(fake, command, default_category):
    thread = get_fake_thread(fake, default_category)
    command.create_fake_post(fake, timezone.now())
    assert thread.post_set.count() == 2


def test_fake_post_creation_date_is_overridden_by_command(
    fake, command, date, default_category
):
    thread = get_fake_thread(fake, default_category)
    thread.started_on -= timedelta(days=1)
    thread.save()

    command.create_fake_post(fake, date)
    post = thread.post_set.last()
    assert post.posted_on == date


def test_fake_post_is_not_created_if_no_threads_exist(fake, command, date):
    command.create_fake_post(fake, date)
    assert not Post.objects.exists()


def test_management_command_synchronizes_threads(fake, command, date, default_category):
    command.create_fake_thread(fake, date, [default_category])
    command.synchronize_threads()


def test_management_command_synchronizes_categories(
    fake, command, date, default_category
):
    command.create_fake_thread(fake, date, [default_category])
    command.synchronize_threads()
    command.synchronize_categories()
