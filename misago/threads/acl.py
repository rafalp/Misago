from django.utils.translation import ugettext_lazy as _
from django import forms
from misago.acl.builder import BaseACL
from misago.acl.utils import ACLError403, ACLError404
from misago.forms import YesNoSwitch

def make_forum_form(request, role, form):
    form.base_fields['can_read_threads'] = forms.ChoiceField(choices=(
                                                                     ('0', _("No")),
                                                                     ('1', _("Yes, owned")),
                                                                     ('2', _("Yes, all")),
                                                                     ))
    form.base_fields['can_start_threads'] = forms.ChoiceField(choices=(
                                                                       ('0', _("No")),
                                                                       ('1', _("Yes, with moderation")),
                                                                       ('2', _("Yes")),
                                                                       ))
    form.base_fields['can_edit_own_threads'] = forms.BooleanField(widget=YesNoSwitch,initial=False,required=False)
    form.base_fields['can_soft_delete_own_threads'] = forms.BooleanField(widget=YesNoSwitch,initial=False,required=False)
    form.base_fields['can_write_posts'] = forms.ChoiceField(choices=(
                                                                     ('0', _("No")),
                                                                     ('1', _("Yes, with moderation")),
                                                                     ('2', _("Yes")),
                                                                     ))
    form.base_fields['can_edit_own_posts'] = forms.BooleanField(widget=YesNoSwitch,initial=False,required=False)
    form.base_fields['can_soft_delete_own_posts'] = forms.BooleanField(widget=YesNoSwitch,initial=False,required=False)
    form.base_fields['can_upvote_posts'] = forms.BooleanField(widget=YesNoSwitch,initial=False,required=False)
    form.base_fields['can_downvote_posts'] = forms.BooleanField(widget=YesNoSwitch,initial=False,required=False)
    form.base_fields['can_see_posts_scores'] = forms.ChoiceField(choices=(
                                                                          ('0', _("No")),
                                                                          ('1', _("Yes, final score")),
                                                                          ('2', _("Yes, both up and down-votes")),
                                                                          ))
    form.base_fields['can_see_votes'] = forms.BooleanField(widget=YesNoSwitch,initial=False,required=False)
    form.base_fields['can_make_polls'] = forms.BooleanField(widget=YesNoSwitch,initial=False,required=False)
    form.base_fields['can_vote_in_polls'] = forms.BooleanField(widget=YesNoSwitch,initial=False,required=False)
    form.base_fields['can_see_votes'] = forms.BooleanField(widget=YesNoSwitch,initial=False,required=False)
    form.base_fields['can_see_attachments'] = forms.BooleanField(widget=YesNoSwitch,initial=False,required=False)
    form.base_fields['can_upload_attachments'] = forms.BooleanField(widget=YesNoSwitch,initial=False,required=False)
    form.base_fields['can_download_attachments'] = forms.BooleanField(widget=YesNoSwitch,initial=False,required=False)
    form.base_fields['attachment_size'] = forms.IntegerField(min_value=0,initial=100)
    form.base_fields['attachment_limit'] = forms.IntegerField(min_value=0,initial=3)
    form.base_fields['can_approve'] = forms.BooleanField(widget=YesNoSwitch,initial=False,required=False)
    form.base_fields['can_edit_labels'] = forms.BooleanField(widget=YesNoSwitch,initial=False,required=False)
    form.base_fields['can_see_changelog'] = forms.BooleanField(widget=YesNoSwitch,initial=False,required=False)
    form.base_fields['can_make_annoucements'] = forms.BooleanField(widget=YesNoSwitch,initial=False,required=False)
    form.base_fields['can_pin_threads'] = forms.BooleanField(widget=YesNoSwitch,initial=False,required=False)
    form.base_fields['can_edit_threads_posts'] = forms.BooleanField(widget=YesNoSwitch,initial=False,required=False)
    form.base_fields['can_move_threads_posts'] = forms.BooleanField(widget=YesNoSwitch,initial=False,required=False)
    form.base_fields['can_close_threads'] = forms.BooleanField(widget=YesNoSwitch,initial=False,required=False)
    form.base_fields['can_protect_posts'] = forms.BooleanField(widget=YesNoSwitch,initial=False,required=False)
    form.base_fields['can_delete_threads'] = forms.ChoiceField(choices=(
                                                                        ('0', _("No")),
                                                                        ('1', _("Yes, soft-delete")),
                                                                        ('2', _("Yes, hard-delete")),
                                                                        ))
    form.base_fields['can_delete_posts'] = forms.ChoiceField(choices=(
                                                                      ('0', _("No")),
                                                                      ('1', _("Yes, soft-delete")),
                                                                      ('2', _("Yes, hard-delete")),
                                                                      ))
    form.base_fields['can_delete_polls'] = forms.ChoiceField(choices=(
                                                                      ('0', _("No")),
                                                                      ('1', _("Yes, soft-delete")),
                                                                      ('2', _("Yes, hard-delete")),
                                                                      ))
    form.base_fields['can_delete_attachments'] = forms.BooleanField(widget=YesNoSwitch,initial=False,required=False)
    
    form.layout.append((
                        _("Threads"),
                        (
                         ('can_read_threads', {'label': _("Can read threads")}),
                         ('can_start_threads', {'label': _("Can start new threads")}),
                         ('can_edit_own_threads', {'label': _("Can edit own threads")}),
                         ('can_soft_delete_own_threads', {'label': _("Can soft-delete own threads")}),
                        ),
                       ),)
    form.layout.append((
                        _("Posts"),
                        (
                         ('can_write_posts', {'label': _("Can write posts")}),
                         ('can_edit_own_posts', {'label': _("Can edit own posts")}),
                         ('can_edit_own_posts', {'label': _("Can soft-delete own posts")}),
                        ),
                       ),)
    form.layout.append((
                        _("Karma"),
                        (
                         ('can_upvote_posts', {'label': _("Can upvote posts")}),
                         ('can_downvote_posts', {'label': _("Can downvote posts")}),
                         ('can_see_posts_scores', {'label': _("Can see post score")}),
                         ('can_see_votes', {'label': _("Can see who voted on post")}),
                        ),
                       ),)
    form.layout.append((
                        _("Polls"),
                        (
                         ('can_make_polls', {'label': _("Can make polls")}),
                         ('can_vote_in_polls', {'label': _("Can vote in polls")}),
                         ('can_see_votes', {'label': _("Can see who voted in poll")}),
                        ),
                       ),)
    form.layout.append((
                        _("Attachments"),
                        (
                         ('can_see_attachments', {'label': _("Can see attachments")}),
                         ('can_upload_attachments', {'label': _("Can upload attachments")}),
                         ('can_download_attachments', {'label': _("Can download attachments")}),
                         ('attachment_size', {'label': _("Max size of single attachment (in Kb)"), 'help_text': _("Enter zero for no limit.")}),
                         ('attachment_limit', {'label': _("Max number of attachments per post"), 'help_text': _("Enter zero for no limit.")}),
                        ),
                       ),)
    form.layout.append((
                        _("Moderation"),
                        (
                         ('can_approve', {'label': _("Can accept threads and posts")}),
                         ('can_edit_labels', {'label': _("Can edit thread labels")}),
                         ('can_see_changelog', {'label': _("Can see edits history")}),
                         ('can_make_annoucements', {'label': _("Can make annoucements")}),
                         ('can_pin_threads', {'label': _("Can pin threads")}),
                         ('can_edit_threads_posts', {'label': _("Can edit threads and posts")}),
                         ('can_move_threads_posts', {'label': _("Can move, merge and split threads and posts")}),
                         ('can_close_threads', {'label': _("Can close threads")}),
                         ('can_protect_posts', {'label': _("Can protect posts"), 'help_text': _("Protected posts cannot be changed by their owners.")}),
                         ('can_delete_threads', {'label': _("Can delete threads")}),
                         ('can_delete_posts', {'label': _("Can delete posts")}),
                         ('can_delete_polls', {'label': _("Can delete polls")}),
                         ('can_delete_attachments', {'label': _("Can delete attachments")}),
                        ),
                       ),)


class ThreadsACL(BaseACL):
    def can_start_threads(self, forum):
        try:
            forum_role = self.acl[forum.pk]
            if not forum_role['can_read_threads'] or not not forum_role['can_read_threads']:
                return False
            if forum.closed and not forum_role['can_close_threads']:
                return False
            return True
        except KeyError:
            return False
    
    def allow_new_threads(self, forum):
        try:
            forum_role = self.acl[forum.pk]
            if not forum_role['can_read_threads'] or not not forum_role['can_read_threads']:
                raise ACLError403(_("You don't have permission to start new threads in this forum."))
            if forum.closed and not forum_role['can_close_threads']:
                raise ACLError403(_("This forum is closed, you can't start new threads in it."))
        except KeyError:
            raise ACLError403(_("You don't have permission to start new threads in this forum."))

 
def build_forums(acl, perms, forums, forum_roles):
    acl.threads = ThreadsACL()
    for forum in forums:
        forum_role = {
                     'can_read_threads': 0,
                     'can_start_threads': 0,
                     'can_edit_own_threads': False,
                     'can_soft_delete_own_threads': False,
                     'can_write_posts': 0,
                     'can_edit_own_posts': False,
                     'can_soft_delete_own_posts': False,
                     'can_upvote_posts': False,
                     'can_downvote_posts': False,
                     'can_see_posts_scores': 0,
                     'can_see_votes': False,
                     'can_make_polls': False,
                     'can_vote_in_polls': False,
                     'can_see_votes': False,
                     'can_see_attachments': False,
                     'can_upload_attachments': False,
                     'can_download_attachments': False,
                     'attachment_size': 100,
                     'attachment_limit': 3,
                     'can_approve': False,
                     'can_edit_labels': False,
                     'can_see_changelog': False,
                     'can_make_annoucements': False,
                     'can_pin_threads': False,
                     'can_edit_threads_posts': False,
                     'can_move_threads_posts': False,
                     'can_close_threads': False,
                     'can_protect_posts': False,
                     'can_delete_threads': 0,
                     'can_delete_posts': 0,
                     'can_delete_polls': 0,
                     'can_delete_attachments': False,
                     }
        for perm in perms:
            try:
                role = forum_roles[perm['forums'][forum.pk]]
                for p in forum_role:
                    if p in ['attachment_size', 'attachment_limit'] and role[p] == 0:
                        forum_role[p] = 0
                    elif role[p] > forum_role[p]:
                        forum_role[p] = role[p]
            except KeyError:
                pass
        acl.threads.acl[forum.pk] = forum_role
            