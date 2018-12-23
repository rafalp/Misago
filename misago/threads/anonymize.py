from django.urls import reverse

ANONYMIZABLE_EVENTS = (
    "added_participant",
    "changed_owner",
    "owner_left",
    "removed_owner",
    "participant_left",
    "removed_participant",
)


def anonymize_event(user, event):
    if event.event_type not in ANONYMIZABLE_EVENTS:
        raise ValueError('event of type "%s" can\'t be ananymized' % event.event_type)

    event.event_context = {
        "user": {"id": None, "username": user.username, "url": reverse("misago:index")}
    }
    event.save(update_fields=["event_context"])


def anonymize_post_last_likes(user, post):
    cleaned_likes = []
    for like in post.last_likes:
        if like["id"] == user.id:
            cleaned_likes.append({"id": None, "username": user.username})
        else:
            cleaned_likes.append(like)

    if cleaned_likes != post.last_likes:
        post.last_likes = cleaned_likes
        post.save(update_fields=["last_likes"])
