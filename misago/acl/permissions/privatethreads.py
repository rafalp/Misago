from django.utils.translation import ugettext_lazy as _
import floppyforms as forms
from misago.acl.builder import BaseACL
from misago.acl.exceptions import ACLError403, ACLError404
from misago.forms import YesNoSwitch
from misago.models import Forum

def make_form(request, role, form):
    if role.special != 'guest':
        form.base_fields['can_use_private_threads'] = forms.BooleanField(widget=YesNoSwitch, initial=False, required=False)
        form.base_fields['can_start_private_threads'] = forms.BooleanField(widget=YesNoSwitch, initial=False, required=False)
        form.base_fields['can_upload_attachments_in_private_threads'] = forms.BooleanField(widget=YesNoSwitch, initial=False, required=False)
        form.base_fields['private_thread_attachment_size'] = forms.IntegerField(min_value=0, initial=100, required=False)
        form.base_fields['private_thread_attachments_limit'] = forms.IntegerField(min_value=0, initial=3, required=False)
        form.base_fields['can_invite_ignoring'] = forms.BooleanField(widget=YesNoSwitch, initial=False, required=False)
        form.base_fields['private_threads_mod'] = forms.BooleanField(widget=YesNoSwitch, initial=False, required=False)
        form.base_fields['can_delete_checkpoints'] = forms.TypedChoiceField(choices=(
                                                                                     (0, _("No")),
                                                                                     (1, _("Yes, soft-delete")),
                                                                                     (2, _("Yes, hard-delete")),
                                                                                     ), coerce=int)

        form.layout.append((
                            _("Private Threads"),
                            (
                             ('can_use_private_threads', {'label': _("Can participate in private threads")}),
                             ('can_start_private_threads', {'label': _("Can start private threads")}),
                             ('can_upload_attachments_in_private_threads', {'label': _("Can upload files in attachments")}),
                             ('private_thread_attachment_size', {'label': _("Max. size of single attachment (in KB)")}),
                             ('private_thread_attachments_limit', {'label': _("Max. number of attachments per post")}),
                             ('can_invite_ignoring', {'label': _("Can invite users that ignore him")}),
                             ('private_threads_mod', {'label': _("Can moderate threads"), 'help_text': _("Makes user with this role Private Threads moderator capable of closing, deleting and editing all private threads he participates in at will.")}),
                             ('can_delete_checkpoints', {'label': _("Can delete checkpoints")}),
                             ),
                            ))


class PrivateThreadsACL(BaseACL):
    def can_start(self):
        return (self.acl['can_use_private_threads'] and
                self.acl['can_start_private_threads'])

    def can_participate(self):
        return self.acl['can_use_private_threads']
        
    def can_invite_ignoring(self):
        return self.acl['can_invite_ignoring']
        
    def is_mod(self):
        return self.acl['private_threads_mod']


def build(acl, roles):
    acl.private_threads = PrivateThreadsACL()
    acl.private_threads.acl['can_use_private_threads'] = False
    acl.private_threads.acl['can_start_private_threads'] = False
    acl.private_threads.acl['can_upload_attachments_in_private_threads'] = False
    acl.private_threads.acl['private_thread_attachment_size'] = False
    acl.private_threads.acl['private_thread_attachments_limit'] = False
    acl.private_threads.acl['can_invite_ignoring'] = False
    acl.private_threads.acl['private_threads_mod'] = False
    acl.private_threads.acl['can_delete_checkpoints'] = 0
    acl.private_threads.acl['can_see_deleted_checkpoints'] = False

    for role in roles:
        for perm, value in acl.private_threads.acl.items():
            if perm in role and role[perm] > value:
                acl.private_threads.acl[perm] = role[perm]


def cleanup(acl, perms, forums):
    forum = Forum.objects.special_pk('private_threads')
    acl.threads.acl[forum] = {
                              'can_read_threads': 2,
                              'can_start_threads': 0,
                              'can_edit_own_threads': True,
                              'can_soft_delete_own_threads': False,
                              'can_write_posts': 2,
                              'can_edit_own_posts': True,
                              'can_soft_delete_own_posts': True,
                              'can_upvote_posts': False,
                              'can_downvote_posts': False,
                              'can_see_posts_scores': 0,
                              'can_see_votes': False,
                              'can_make_polls': False,
                              'can_vote_in_polls': False,
                              'can_see_poll_votes': False,
                              'can_see_attachments': True,
                              'can_upload_attachments': False,
                              'can_download_attachments': True,
                              'attachment_size': 100,
                              'attachment_limit': 3,
                              'can_approve': False,
                              'can_edit_labels': False,
                              'can_see_changelog': False,
                              'can_pin_threads': 0,
                              'can_edit_threads_posts': False,
                              'can_move_threads_posts': False,
                              'can_close_threads': False,
                              'can_protect_posts': False,
                              'can_delete_threads': 0,
                              'can_delete_posts': 0,
                              'can_delete_polls': 0,
                              'can_delete_attachments': False,
                              'can_invite_ignoring': False,
                              'can_delete_checkpoints': 0,
                              'can_see_deleted_checkpoints': False,
                             }

    for perm in perms:
        try:
            if perm['can_use_private_threads'] and forum not in acl.forums.acl['can_see']:
                acl.forums.acl['can_see'].append(forum)
                acl.forums.acl['can_browse'].append(forum)
            if perm['can_start_private_threads']:
                acl.threads.acl[forum]['can_start_threads'] = 2
            if perm['can_upload_attachments_in_private_threads']:
                acl.threads.acl[forum]['can_upload_attachments'] = True
            if perm['private_thread_attachment_size']:
                acl.threads.acl[forum]['attachment_size'] = True
            if perm['private_thread_attachments_limit']:
                acl.threads.acl[forum]['attachment_limit'] = True
            if perm['can_invite_ignoring']:
                acl.threads.acl[forum]['can_invite_ignoring'] = True
            if perm['private_threads_mod']:
                acl.threads.acl[forum]['can_close_threads'] = True
                acl.threads.acl[forum]['can_protect_posts'] = True
                acl.threads.acl[forum]['can_edit_threads_posts'] = True
                acl.threads.acl[forum]['can_move_threads_posts'] = True
                acl.threads.acl[forum]['can_see_changelog'] = True
                acl.threads.acl[forum]['can_delete_threads'] = 2
                acl.threads.acl[forum]['can_delete_posts'] = 2
                acl.threads.acl[forum]['can_delete_attachments'] = True
                acl.threads.acl[forum]['can_see_deleted_checkpoints'] = True
            if perm['can_delete_checkpoints'] > acl.threads.acl[forum]['can_delete_checkpoints']:
                acl.threads.acl[forum]['can_delete_checkpoints'] = perm['can_delete_checkpoints']
        except KeyError:
            pass
