from django.db.transaction import atomic
from django.utils.translation import ugettext as _

from misago.threads.moderation.exceptions import ModerationError


@atomic
def unhide_post(user, post):
    if post.pk == post.thread.first_post_id:
        raise ModerationError(_("You can't make original post "
                                " visible without revealing thread."))

    if post.is_hidden:
        post.is_hidden = False
        post.save(update_fields=['is_hidden'])
        return True
    else:
        return False


@atomic
def hide_post(user, post):
    if post.pk == post.thread.first_post_id:
        raise ModerationError(_("You can't hide original "
                                "post without hiding thread."))

    if not post.is_hidden:
        post.is_hidden = True
        post.save(update_fields=['is_hidden'])
        return True
    else:
        return False


@atomic
def delete_post(user, post):
    if post.pk == post.thread.first_post_id:
        raise ModerationError(_("You can't delete original "
                                "post without deleting thread."))

    post.delete()
    return True
