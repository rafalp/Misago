from django import template
from django.utils.translation import npgettext, pgettext

register = template.Library()


@register.simple_tag
def likes_label(post):
    last_likes = post.last_likes or []

    usernames = []
    for like in last_likes[:3]:
        usernames.append(like["username"])

    if len(usernames) == 1:
        return pgettext("post likes message", "%(user)s likes this.") % {
            "user": usernames[0]
        }

    hidden_likes = post.likes - len(usernames)
    if len(last_likes) < 4:
        usernames_string = humanize_usernames_list(usernames)
    else:
        usernames_string = ", ".join(usernames)

    if not hidden_likes:
        return pgettext("post likes message", "%(users)s like this.") % {
            "users": usernames_string
        }

    label = npgettext(
        "post likes message",
        "%(users)s and %(likes)s other user like this.",
        "%(users)s and %(likes)s other users like this.",
        hidden_likes,
    )
    formats = {"users": usernames_string, "likes": hidden_likes}

    return label % formats


def humanize_usernames_list(usernames):
    formats = {"users": ", ".join(usernames[:-1]), "last_user": usernames[-1]}

    return pgettext("post likes message", "%(users)s and %(last_user)s") % formats
