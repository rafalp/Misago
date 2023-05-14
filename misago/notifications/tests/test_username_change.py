from ..models import Notification


def test_notification_actor_name_is_updated_on_username_change(user, other_user):
    notification = Notification.objects.create(
        user=user,
        actor=other_user,
        actor_name=other_user.username,
        verb="TEST",
    )

    other_user.set_username("ChangedName")

    notification.refresh_from_db()
    assert notification.actor_name == "ChangedName"
