from django.db.transaction import atomic
from django.utils import timezone
from django.utils.translation import ugettext as _

from misago.threads.moderation.exceptions import ModerationError


def protect_post(user, post):
    if not post.is_protected:
        post.is_protected = True
        post.save(update_fields=['is_protected'])
        return True
    else:
        return False


def unprotect_post(user, post):
    if post.is_protected:
        post.is_protected = False
        post.save(update_fields=['is_protected'])
        return True
    else:
        return False


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


def hide_post(user, post):
    if post.pk == post.thread.first_post_id:
        raise ModerationError(_("You can't hide original "
                                "post without hiding thread."))

    if not post.is_hidden:
        post.is_hidden = True
        post.hidden_by = user
        post.hidden_by_name = user.username
        post.hidden_by_slug = user.slug
        post.hidden_on = timezone.now()
        post.save(update_fields=[
            'is_hidden',
            'hidden_by',
            'hidden_by_name',
            'hidden_by_slug',
            'hidden_on',
        ])
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
