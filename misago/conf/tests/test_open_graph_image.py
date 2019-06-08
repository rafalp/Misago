from ...test import assert_contains, assert_not_contains
from ...threads.test import post_thread
from ..models import Setting
from ..test import override_dynamic_settings


@override_dynamic_settings(forum_address="http://test.com/")
def test_default_og_image_is_used_when_none_is_set(db, client):
    response = client.get("/")
    assert_contains(response, "http://test.com/static/misago/img/og-image.jpg")


@override_dynamic_settings(forum_address="http://test.com/")
def test_custom_og_image_is_used_instead_of_default_one_when_set(db, client):
    Setting.objects.filter(setting="og_image").update(
        image="custom-image.jpg", image_width=600, image_height=300
    )

    response = client.get("/")
    assert_not_contains(response, "http://test.com/media/misago/img/og-image.jpg")
    assert_contains(response, "http://test.com/media/custom-image.jpg")
    assert_contains(response, 'property="og:image:width" content="600"')
    assert_contains(response, 'property="og:image:height" content="300"')


@override_dynamic_settings(forum_address="http://test.com/")
def test_default_og_image_is_used_on_user_profiles(client, user):
    response = client.get("%sposts/" % user.get_absolute_url())
    assert_contains(response, "http://test.com/static/misago/img/og-image.jpg")


@override_dynamic_settings(
    forum_address="http://test.com/", og_image_avatar_on_profile=True
)
def test_user_avatar_can_be_used_as_og_image_on_user_profiles(client, user):
    response = client.get("%sposts/" % user.get_absolute_url())
    assert_not_contains(response, "http://test.com/static/misago/img/og-image.jpg")


@override_dynamic_settings(forum_address="http://test.com/")
def test_default_og_image_is_used_on_thread_page(client, default_category, user):
    thread = post_thread(default_category, poster=user)
    response = client.get(thread.get_absolute_url())
    assert_contains(response, "http://test.com/static/misago/img/og-image.jpg")


@override_dynamic_settings(
    forum_address="http://test.com/", og_image_avatar_on_thread=True
)
def test_thread_started_avatar_can_be_used_as_og_image_on_thread_page(
    client, default_category, user
):
    thread = post_thread(default_category, poster=user)
    response = client.get(thread.get_absolute_url())
    assert_not_contains(response, "http://test.com/static/misago/img/og-image.jpg")
