from ..models import Notification


def test_notification_actor_name_is_anonymized(user, other_user):
    notification = Notification.objects.create(
        user=user,
        actor=other_user,
        actor_name=other_user.username,
        verb="TEST",
    )

    other_user.anonymize_data("Deleted")

    notification.refresh_from_db()
    assert notification.actor_name == "Deleted"
