from misago.forumroles.models import ForumRole
from misago.utils import ugettext_lazy as _
from misago.utils import get_msgid

def load_fixtures():
    role = ForumRole()
    role.name = _('Full Access').message
    role.set_permissions({
                          'can_see_forum': True,
                          'can_see_forum_contents': True,
                          'can_read_threads': '2',
                          'can_start_threads': '2',
                          'can_edit_own_threads': True,
                          'can_soft_delete_own_threads': True,
                          'can_write_posts': '2',
                          'can_edit_own_posts': True,
                          'can_soft_delete_own_posts': True,
                          'can_upvote_posts': True,
                          'can_downvote_posts': True,
                          'can_see_posts_scores': '2',
                          'can_see_votes': True,
                          'can_make_polls': True,
                          'can_vote_in_polls': True,
                          'can_see_poll_votes': True,
                          'can_see_attachments': True,
                          'can_upload_attachments': True,
                          'can_download_attachments': True,
                          'attachment_size': 5000,
                          'attachment_limit': 15,
                          'can_approve': True,
                          'can_edit_labels': True,
                          'can_see_changelog': True,
                          'can_pin_threads': '2',
                          'can_edit_threads_posts': True,
                          'can_move_threads_posts': True,
                          'can_close_threads': True,
                          'can_protect_posts': True,
                          'can_delete_threads': '2',
                          'can_delete_posts': '2',
                          'can_delete_polls': '2',
                          'can_delete_attachments': True,
                          })
    role.save(force_insert=True)

    role = ForumRole()
    role.name = _('Standard Access and Upload').message
    role.set_permissions({
                          'can_see_forum': True,
                          'can_see_forum_contents': True,
                          'can_read_threads': '2',
                          'can_start_threads': '2',
                          'can_edit_own_threads': True,
                          'can_write_posts': '2',
                          'can_edit_own_posts': True,
                          'can_soft_delete_own_posts': True,
                          'can_upvote_posts': True,
                          'can_downvote_posts': True,
                          'can_make_polls': True,
                          'can_vote_in_polls': True,
                          'can_upload_attachments': True,
                          'can_download_attachments': True,
                          'attachment_size': 100,
                          'attachment_limit': 3,
                          })
    role.save(force_insert=True)

    role = ForumRole()
    role.name = _('Standard Access').message
    role.set_permissions({
                          'can_see_forum': True,
                          'can_see_forum_contents': True,
                          'can_read_threads': '2',
                          'can_start_threads': '2',
                          'can_edit_own_threads': True,
                          'can_write_posts': '2',
                          'can_edit_own_posts': True,
                          'can_soft_delete_own_posts': True,
                          'can_upvote_posts': True,
                          'can_downvote_posts': True,
                          'can_make_polls': True,
                          'can_vote_in_polls': True,
                          'can_download_attachments': True,
                          })
    role.save(force_insert=True)

    role = ForumRole()
    role.name = _('Read and Download').message
    role.set_permissions({
                          'can_see_forum': True,
                          'can_see_forum_contents': True,
                          'can_read_threads': '2',
                          'can_download_attachments': True,
                          })
    role.save(force_insert=True)

    role = ForumRole()
    role.name = _('Threads list only').message
    role.set_permissions({
                          'can_see_forum': True,
                          'can_see_forum_contents': True,
                          })
    role.save(force_insert=True)

    role = ForumRole()
    role.name = _('Read only').message
    role.set_permissions({
                          'can_see_forum': True,
                          'can_see_forum_contents': True,
                          'can_read_threads': '2',
                          })
    role.save(force_insert=True)
