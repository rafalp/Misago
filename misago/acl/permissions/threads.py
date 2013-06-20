from django import forms
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from misago.acl.builder import BaseACL
from misago.acl.exceptions import ACLError403, ACLError404
from misago.forms import YesNoSwitch

def make_forum_form(request, role, form):
    form.base_fields['can_read_threads'] = forms.TypedChoiceField(choices=(
                                                                  (0, _("No")),
                                                                  (1, _("Yes, owned")),
                                                                  (2, _("Yes, all")),
                                                                  ), coerce=int)
    form.base_fields['can_start_threads'] = forms.TypedChoiceField(choices=(
                                                                   (0, _("No")),
                                                                   (1, _("Yes, with moderation")),
                                                                   (2, _("Yes")),
                                                                   ), coerce=int)
    form.base_fields['can_edit_own_threads'] = forms.BooleanField(widget=YesNoSwitch, initial=False, required=False)
    form.base_fields['can_soft_delete_own_threads'] = forms.BooleanField(widget=YesNoSwitch, initial=False, required=False)
    form.base_fields['can_write_posts'] = forms.TypedChoiceField(choices=(
                                                                 (0, _("No")),
                                                                 (1, _("Yes, with moderation")),
                                                                 (2, _("Yes")),
                                                                 ), coerce=int)
    form.base_fields['can_edit_own_posts'] = forms.BooleanField(widget=YesNoSwitch, initial=False, required=False)
    form.base_fields['can_soft_delete_own_posts'] = forms.BooleanField(widget=YesNoSwitch, initial=False, required=False)
    form.base_fields['can_upvote_posts'] = forms.BooleanField(widget=YesNoSwitch, initial=False, required=False)
    form.base_fields['can_downvote_posts'] = forms.BooleanField(widget=YesNoSwitch, initial=False, required=False)
    form.base_fields['can_see_posts_scores'] = forms.TypedChoiceField(choices=(
                                                                      (0, _("No")),
                                                                      (1, _("Yes, final score")),
                                                                      (2, _("Yes, both up and down-votes")),
                                                                      ), coerce=int)
    form.base_fields['can_see_votes'] = forms.BooleanField(widget=YesNoSwitch, initial=False, required=False)
    form.base_fields['can_make_polls'] = forms.BooleanField(widget=YesNoSwitch, initial=False, required=False)
    form.base_fields['can_vote_in_polls'] = forms.BooleanField(widget=YesNoSwitch, initial=False, required=False)
    form.base_fields['can_see_poll_votes'] = forms.BooleanField(widget=YesNoSwitch, initial=False, required=False)
    form.base_fields['can_see_attachments'] = forms.BooleanField(widget=YesNoSwitch, initial=False, required=False)
    form.base_fields['can_upload_attachments'] = forms.BooleanField(widget=YesNoSwitch, initial=False, required=False)
    form.base_fields['can_download_attachments'] = forms.BooleanField(widget=YesNoSwitch, initial=False, required=False)
    form.base_fields['attachment_size'] = forms.IntegerField(min_value=0, initial=100)
    form.base_fields['attachment_limit'] = forms.IntegerField(min_value=0, initial=3)
    form.base_fields['can_approve'] = forms.BooleanField(widget=YesNoSwitch, initial=False, required=False)
    form.base_fields['can_edit_labels'] = forms.BooleanField(widget=YesNoSwitch, initial=False, required=False)
    form.base_fields['can_see_changelog'] = forms.BooleanField(widget=YesNoSwitch, initial=False, required=False)
    form.base_fields['can_pin_threads'] = forms.TypedChoiceField(choices=(
                                                                          (0, _("No")),
                                                                          (1, _("Yes, to stickies")),
                                                                          (2, _("Yes, to announcements")),
                                                                          ), coerce=int)
    form.base_fields['can_edit_threads_posts'] = forms.BooleanField(widget=YesNoSwitch, initial=False, required=False)
    form.base_fields['can_move_threads_posts'] = forms.BooleanField(widget=YesNoSwitch, initial=False, required=False)
    form.base_fields['can_close_threads'] = forms.BooleanField(widget=YesNoSwitch, initial=False, required=False)
    form.base_fields['can_protect_posts'] = forms.BooleanField(widget=YesNoSwitch, initial=False, required=False)
    form.base_fields['can_delete_threads'] = forms.TypedChoiceField(choices=(
                                                                             (0, _("No")),
                                                                             (1, _("Yes, soft-delete")),
                                                                             (2, _("Yes, hard-delete")),
                                                                             ), coerce=int)
    form.base_fields['can_delete_posts'] = forms.TypedChoiceField(choices=(
                                                                           (0, _("No")),
                                                                           (1, _("Yes, soft-delete")),
                                                                           (2, _("Yes, hard-delete")),
                                                                           ), coerce=int)
    form.base_fields['can_delete_polls'] = forms.TypedChoiceField(choices=(
                                                                           (0, _("No")),
                                                                           (1, _("Yes, soft-delete")),
                                                                           (2, _("Yes, hard-delete")),
                                                                           ), coerce=int)
    form.base_fields['can_delete_attachments'] = forms.BooleanField(widget=YesNoSwitch, initial=False, required=False)
    form.base_fields['can_delete_checkpoints'] = forms.TypedChoiceField(choices=(
                                                                                 (0, _("No")),
                                                                                 (1, _("Yes, soft-delete")),
                                                                                 (2, _("Yes, hard-delete")),
                                                                                 ), coerce=int)
    form.base_fields['can_see_deleted_checkpoints'] = forms.BooleanField(widget=YesNoSwitch, initial=False, required=False)

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
                         ('can_soft_delete_own_posts', {'label': _("Can soft-delete own posts")}),
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
                         ('can_see_poll_votes', {'label': _("Can see who voted in poll")}),
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
                         ('can_pin_threads', {'label': _("Can change threads weight")}),
                         ('can_edit_threads_posts', {'label': _("Can edit threads and posts")}),
                         ('can_move_threads_posts', {'label': _("Can move, merge and split threads and posts")}),
                         ('can_close_threads', {'label': _("Can close threads")}),
                         ('can_protect_posts', {'label': _("Can protect posts"), 'help_text': _("Protected posts cannot be changed by their owners.")}),
                         ('can_delete_threads', {'label': _("Can delete threads")}),
                         ('can_delete_posts', {'label': _("Can delete posts")}),
                         ('can_delete_polls', {'label': _("Can delete polls")}),
                         ('can_delete_attachments', {'label': _("Can delete attachments")}),
                         ('can_delete_checkpoints', {'label': _("Can delete checkpoints")}),
                         ('can_see_deleted_checkpoints', {'label': _("Can see deleted checkpoints")}),
                        ),
                       ),)


class ThreadsACL(BaseACL):
    def get_role(self, forum):
        try:
            try:
                return self.acl[forum.pk]
            except AttributeError:
                return self.acl[forum]
        except KeyError:
            return {}

    def allow_thread_view(self, user, thread):
        try:
            forum_role = self.acl[thread.forum_id]
            if forum_role['can_read_threads'] == 0:
                raise ACLError403(_("You don't have permission to read threads in this forum."))
            if forum_role['can_read_threads'] == 1 and thread.weight < 2 and thread.start_poster_id != user.id:
                raise ACLError404()
            if thread.moderated and not (forum_role['can_approve'] or (user.is_authenticated() and user == thread.start_poster)):
                raise ACLError404()
            if thread.deleted and not forum_role['can_delete_threads']:
                raise ACLError404()
        except KeyError:
            raise ACLError403(_("You don't have permission to read threads in this forum."))

    def allow_post_view(self, user, thread, post):
        forum_role = self.acl[thread.forum_id]
        if post.moderated and not (forum_role['can_approve'] or (user.is_authenticated() and user == post.user)):
            raise ACLError404()
        if post.deleted and not (forum_role['can_delete_posts'] or (user.is_authenticated() and user == post.user)):
            raise ACLError404()

    def filter_threads(self, request, forum, queryset):
        try:
            forum_role = self.acl[forum.pk]
            if not forum_role['can_approve']:
                if request.user.is_authenticated():
                    queryset = queryset.filter(Q(moderated=False) | Q(start_poster=request.user))
                else:
                    queryset = queryset.filter(moderated=False)
            if forum_role['can_read_threads'] == 1:
                queryset = queryset.filter(Q(weight=2) | Q(start_poster_id=request.user.id))
            if not forum_role['can_delete_threads']:
                queryset = queryset.filter(deleted=False)
        except KeyError:
            return False
        return queryset

    def filter_posts(self, request, thread, queryset):
        try:
            forum_role = self.acl[thread.forum.pk]
            if not forum_role['can_approve']:
                if request.user.is_authenticated():
                    queryset = queryset.filter(Q(moderated=0) | Q(user=request.user))
                else:
                    queryset = queryset.filter(moderated=0)
        except KeyError:
            return False
        return queryset

    def can_read_threads(self, forum):
        try:
            forum_role = self.acl[forum.pk]
            return forum_role['can_read_threads']
        except KeyError:
            return False

    def can_start_threads(self, forum):
        try:
            forum_role = self.acl[forum.pk]
            if forum_role['can_read_threads'] == 0 or forum_role['can_start_threads'] == 0:
                return False
            if forum.closed and forum_role['can_close_threads'] == 0:
                return False
            return True
        except KeyError:
            return False

    def allow_new_threads(self, forum):
        try:
            forum_role = self.acl[forum.pk]
            if forum_role['can_read_threads'] == 0 or forum_role['can_start_threads'] == 0:
                raise ACLError403(_("You don't have permission to start new threads in this forum."))
            if forum.closed and forum_role['can_close_threads'] == 0:
                raise ACLError403(_("This forum is closed, you can't start new threads in it."))
        except KeyError:
            raise ACLError403(_("You don't have permission to start new threads in this forum."))

    def can_edit_thread(self, user, forum, thread, post):
        try:
            forum_role = self.acl[thread.forum_id]
            if forum_role['can_close_threads'] == 0 and (forum.closed or thread.closed):
                return False
            if forum_role['can_edit_threads_posts']:
                return True
            if forum_role['can_edit_own_threads'] and not post.protected and post.user_id == user.pk:
                return True
            return False
        except KeyError:
            return False

    def allow_thread_edit(self, user, forum, thread, post):
        try:
            forum_role = self.acl[thread.forum_id]
            if thread.deleted or post.deleted:
                self.allow_deleted_post_view(forum)
            if not forum_role['can_close_threads']:
                if forum.closed:
                    raise ACLError403(_("You can't edit threads in closed forums."))
                if thread.closed:
                    raise ACLError403(_("You can't edit closed threads."))
            if not forum_role['can_edit_threads_posts']:
                if post.user_id != user.pk:
                    raise ACLError403(_("You can't edit other members threads."))
                if not forum_role['can_edit_own_threads']:
                    raise ACLError403(_("You can't edit your threads."))
                if post.protected:
                    raise ACLError403(_("This thread is protected, you cannot edit it."))
        except KeyError:
            raise ACLError403(_("You don't have permission to edit threads in this forum."))

    def can_reply(self, forum, thread):
        try:
            forum_role = self.acl[forum.pk]
            if forum_role['can_write_posts'] == 0:
                return False
            if (forum.closed or thread.closed) and forum_role['can_close_threads'] == 0:
                return False
            return True
        except KeyError:
            return False

    def allow_reply(self, forum, thread):
        try:
            forum_role = self.acl[thread.forum.pk]
            if forum_role['can_write_posts'] == 0:
                raise ACLError403(_("You don't have permission to write replies in this forum."))
            if forum_role['can_close_threads'] == 0:
                if forum.closed:
                    raise ACLError403(_("You can't write replies in closed forums."))
                if thread.closed:
                    raise ACLError403(_("You can't write replies in closed threads."))
        except KeyError:
            raise ACLError403(_("You don't have permission to write replies in this forum."))

    def can_edit_reply(self, user, forum, thread, post):
        try:
            forum_role = self.acl[thread.forum_id]
            if forum_role['can_close_threads'] == 0 and (forum.closed or thread.closed):
                return False
            if forum_role['can_edit_threads_posts']:
                return True
            if forum_role['can_edit_own_posts'] and not post.protected and post.user_id == user.pk:
                return True
            return False
        except KeyError:
            return False

    def allow_reply_edit(self, user, forum, thread, post):
        try:
            forum_role = self.acl[thread.forum_id]
            if thread.deleted or post.deleted:
                self.allow_deleted_post_view(forum)
            if not forum_role['can_close_threads']:
                if forum.closed:
                    raise ACLError403(_("You can't edit replies in closed forums."))
                if thread.closed:
                    raise ACLError403(_("You can't edit replies in closed threads."))
            if not forum_role['can_edit_threads_posts']:
                if post.user_id != user.pk:
                    raise ACLError403(_("You can't edit other members replies."))
                if not forum_role['can_edit_own_posts']:
                    raise ACLError403(_("You can't edit your replies."))
                if post.protected:
                    raise ACLError403(_("This reply is protected, you cannot edit it."))
        except KeyError:
            raise ACLError403(_("You don't have permission to edit replies in this forum."))

    def can_see_changelog(self, user, forum, post):
        try:
            forum_role = self.acl[forum.pk]
            return forum_role['can_see_changelog'] or user.pk == post.user_id
        except KeyError:
            return False

    def allow_changelog_view(self, user, forum, post):
        try:
            forum_role = self.acl[forum.pk]
            if post.thread.deleted or post.deleted:
                self.allow_deleted_post_view(forum)
            if not (forum_role['can_see_changelog'] or user.pk == post.user_id):
                raise ACLError403(_("You don't have permission to see history of changes made to this post."))
        except KeyError:
            raise ACLError403(_("You don't have permission to see history of changes made to this post."))

    def can_make_revert(self, forum, thread):
        try:
            forum_role = self.acl[forum.pk]
            if not forum_role['can_close_threads'] and (forum.closed or thread.closed):
                return False
            return forum_role['can_edit_threads_posts']
        except KeyError:
            return False

    def allow_revert(self, forum, thread):
        try:
            forum_role = self.acl[forum.pk]
            if not forum_role['can_close_threads']:
                if forum.closed:
                    raise ACLError403(_("You can't make reverts in closed forums."))
                if thread.closed:
                    raise ACLError403(_("You can't make reverts in closed threads."))
            if not forum_role['can_edit_threads_posts']:
                raise ACLError403(_("You don't have permission to make reverts in this forum."))
        except KeyError:
            raise ACLError403(_("You don't have permission to make reverts in this forum."))

    def can_mod_threads(self, forum):
        try:
            forum_role = self.acl[forum.pk]
            return (
                    forum_role['can_approve']
                    or forum_role['can_pin_threads']
                    or forum_role['can_move_threads_posts']
                    or forum_role['can_close_threads']
                    or forum_role['can_delete_threads']
                    )
        except KeyError:
            return False

    def can_mod_posts(self, forum):
        try:
            forum_role = self.acl[forum.pk]
            return (
                    forum_role['can_edit_threads_posts']
                    or forum_role['can_move_threads_posts']
                    or forum_role['can_close_threads']
                    or forum_role['can_delete_threads']
                    or forum_role['can_delete_posts']
                    )
        except KeyError:
            return False

    def can_approve(self, forum):
        try:
            forum_role = self.acl[forum.pk]
            return forum_role['can_approve']
        except KeyError:
            return False

    def can_close(self, forum):
        try:
            forum_role = self.acl[forum.pk]
            return forum_role['can_close_threads']
        except KeyError:
            return False

    def can_protect(self, forum):
        try:
            forum_role = self.acl[forum.pk]
            return forum_role['can_protect_posts']
        except KeyError:
            return False

    def can_pin_threads(self, forum):
        try:
            forum_role = self.acl[forum.pk]
            return forum_role['can_pin_threads']
        except KeyError:
            return False

    def can_delete_thread(self, user, forum, thread, post):
        try:
            forum_role = self.acl[forum.pk]
            if post.pk != thread.start_post_id:
                return False
            if not forum_role['can_close_threads'] and (forum.closed or thread.closed):
                return False
            if post.protected and not forum_role['can_protect_posts'] and not forum_role['can_delete_threads']:
                return False
            if forum_role['can_delete_threads']:
                return forum_role['can_delete_threads']
            if thread.start_poster_id == user.pk and forum_role['can_soft_delete_own_threads']:
                return 1
            return False
        except KeyError:
            return False

    def allow_delete_thread(self, user, forum, thread, post, delete=False):
        try:
            forum_role = self.acl[forum.pk]
            if not forum_role['can_close_threads']:
                if forum.closed:
                    raise ACLError403(_("You don't have permission to delete threads in closed forum."))
                if thread.closed:
                    raise ACLError403(_("This thread is closed, you cannot delete it."))
            if post.protected and not forum_role['can_protect_posts'] and not forum_role['can_delete_threads']:
                raise ACLError403(_("This post is protected, you cannot delete it."))
            if not (forum_role['can_delete_threads'] == 2 or
                    (not delete and (forum_role['can_delete_threads'] == 1 or 
                    (thread.start_poster_id == user.pk and forum_role['can_soft_delete_own_threads'])))):
                raise ACLError403(_("You don't have permission to delete this thread."))
            if thread.deleted and not delete:
                raise ACLError403(_("This thread is already deleted."))
        except KeyError:
            raise ACLError403(_("You don't have permission to delete this thread."))

    def can_delete_post(self, user, forum, thread, post):
        try:
            forum_role = self.acl[forum.pk]
            if post.pk == thread.start_post_id:
                return False
            if not forum_role['can_close_threads'] and (forum.closed or thread.closed):
                return False
            if post.protected and not forum_role['can_protect_posts'] and not forum_role['can_delete_posts']:
                return False
            if forum_role['can_delete_posts']:
                return forum_role['can_delete_posts']
            if post.user_id == user.pk and not post.protected and forum_role['can_soft_delete_own_posts']:
                return 1
            return False
        except KeyError:
            return False

    def allow_delete_post(self, user, forum, thread, post, delete=False):
        try:
            forum_role = self.acl[forum.pk]
            if not forum_role['can_close_threads']:
                if forum.closed:
                    raise ACLError403(_("You don't have permission to delete posts in closed forum."))
                if thread.closed:
                    raise ACLError403(_("This thread is closed, you cannot delete its posts."))
            if post.protected and not forum_role['can_protect_posts'] and not forum_role['can_delete_posts']:
                raise ACLError403(_("This post is protected, you cannot delete it."))
            if not (forum_role['can_delete_posts'] == 2 or
                    (not delete and (forum_role['can_delete_posts'] == 1 or 
                    (post.user_id == user.pk and forum_role['can_soft_delete_own_posts'])))):
                raise ACLError403(_("You don't have permission to delete this post."))
            if post.deleted and not delete:
                raise ACLError403(_("This post is already deleted."))
        except KeyError:
            raise ACLError403(_("You don't have permission to delete this post."))

    def can_see_deleted_threads(self, forum):
        try:
            forum_role = self.acl[forum.pk]
            return forum_role['can_delete_threads']
        except KeyError:
            return False

    def can_see_deleted_posts(self, forum):
        try:
            forum_role = self.acl[forum.pk]
            return forum_role['can_delete_posts']
        except KeyError:
            return False

    def allow_deleted_post_view(self, forum):
        try:
            forum_role = self.acl[forum.pk]
            if not forum_role['can_delete_posts']:
                raise ACLError404()
        except KeyError:
            raise ACLError404()
        
    def can_upvote_posts(self, forum):
        try:
            forum_role = self.acl[forum.pk]
            return forum_role['can_upvote_posts']
        except KeyError:
            return False
        
    def can_downvote_posts(self, forum):
        try:
            forum_role = self.acl[forum.pk]
            return forum_role['can_downvote_posts']
        except KeyError:
            return False
        
    def can_see_post_score(self, forum):
        try:
            forum_role = self.acl[forum.pk]
            return forum_role['can_see_posts_scores']
        except KeyError:
            return False
        
    def can_see_post_votes(self, forum):
        try:
            forum_role = self.acl[forum.pk]
            return forum_role['can_see_votes']
        except KeyError:
            return False

    def allow_post_upvote(self, forum):
        try:
            forum_role = self.acl[forum.pk]
            if not forum_role['can_upvote_posts']:
                raise ACLError403(_("You cannot upvote posts in this forum."))
        except KeyError:
            raise ACLError403(_("You cannot upvote posts in this forum."))

    def allow_post_downvote(self, forum):
        try:
            forum_role = self.acl[forum.pk]
            if not forum_role['can_downvote_posts']:
                raise ACLError403(_("You cannot downvote posts in this forum."))
        except KeyError:
            raise ACLError403(_("You cannot downvote posts in this forum."))
        
    def allow_post_votes_view(self, forum):
        try:
            forum_role = self.acl[forum.pk]
            if not forum_role['can_see_votes']:
                raise ACLError403(_("You don't have permission to see who voted on this post."))
        except KeyError:
            raise ACLError403(_("You don't have permission to see who voted on this post."))

    def can_see_all_checkpoints(self, forum):
        try:
            return self.acl[forum.pk]['can_see_deleted_checkpoints']
        except KeyError:
            raise False

    def can_delete_checkpoint(self, forum):
        try:
            return self.acl[forum.pk]['can_delete_checkpoints']
        except KeyError:
            raise False

    def allow_checkpoint_view(self, forum, checkpoint):
        if checkpoint.deleted:
            try:
                forum_role = self.acl[forum.pk]
                if not forum_role['can_see_deleted_checkpoints']:
                    raise ACLError403(_("Selected checkpoint could not be found."))
            except KeyError:
                raise ACLError403(_("Selected checkpoint could not be found."))

    def allow_checkpoint_hide(self, forum):
        try:
            forum_role = self.acl[forum.pk]
            if not forum_role['can_delete_checkpoints']:
                raise ACLError403(_("You cannot hide checkpoints!"))
        except KeyError:
            raise ACLError403(_("You cannot hide checkpoints!"))

    def allow_checkpoint_delete(self, forum):
        try:
            forum_role = self.acl[forum.pk]
            if forum_role['can_delete_checkpoints'] != 2:
                raise ACLError403(_("You cannot delete checkpoints!"))
        except KeyError:
            raise ACLError403(_("You cannot delete checkpoints!"))

    def allow_checkpoint_show(self, forum):
        try:
            forum_role = self.acl[forum.pk]
            if not forum_role['can_delete_checkpoints']:
                raise ACLError403(_("You cannot show checkpoints!"))
        except KeyError:
            raise ACLError403(_("You cannot show checkpoints!"))


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
                     'can_see_poll_votes': False,
                     'can_see_attachments': False,
                     'can_upload_attachments': False,
                     'can_download_attachments': False,
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
                     'can_see_deleted_checkpoints': False,
                     'can_delete_checkpoints': 0,
                     }

        for perm in perms:
            try:
                role = forum_roles[perm['forums'][forum.pk]]
                for p in forum_role:
                    try:
                        if p in ['attachment_size', 'attachment_limit'] and role[p] == 0:
                            forum_role[p] = 0
                        elif role[p] > forum_role[p]:
                            forum_role[p] = role[p]
                    except KeyError:
                        pass
            except KeyError:
                pass
        acl.threads.acl[forum.pk] = forum_role
