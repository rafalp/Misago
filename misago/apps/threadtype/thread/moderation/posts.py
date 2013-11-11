from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.template import RequestContext
from django.utils import timezone
from django.utils.translation import ugettext as _
import floppyforms as forms
from misago import messages
from misago.markdown import post_markdown
from misago.messages import Message
from misago.shortcuts import render_to_response
from misago.utils.strings import slugify
from misago.apps.threadtype.thread.moderation.forms import SplitThreadForm, MovePostsForm

class PostsModeration(object):
    def post_action_accept(self, ids):
        accepted = 0
        for post in self.posts:
            if post.pk in ids and post.moderated:
                accepted += 1
        if accepted:
            self.thread.post_set.filter(id__in=ids).update(moderated=False)
            self.thread.sync()
            self.thread.save(force_update=True)
            messages.success(self.request, _('Selected posts have been accepted and made visible to other members.'), 'threads')
        else:
            messages.info(self.request, _('No posts were accepted.'), 'threads')

    def post_action_merge(self, ids):
        users = []
        posts = []
        for post in self.posts:
            if post.pk in ids:
                posts.append(post)
                if not post.user_id in users:
                    users.append(post.user_id)
                if len(users) > 1:
                    raise forms.ValidationError(_("You cannot merge replies made by different members!"))
        if len(posts) < 2:
            raise forms.ValidationError(_("You have to select two or more posts you want to merge."))
        new_post = posts[0]
        for post in posts[1:]:
            post.merge_with(new_post)
            post.delete()
        md, new_post.post_preparsed = post_markdown(new_post.post)
        new_post.sync_attachments()
        new_post.save(force_update=True)
        self.thread.sync()
        self.thread.save(force_update=True)
        self.forum.sync()
        self.forum.save(force_update=True)
        messages.success(self.request, _('Selected posts have been merged into one message.'), 'threads')

    def post_action_split(self, ids):
        for id in ids:
            if id == self.thread.start_post_id:
                raise forms.ValidationError(_("You cannot split first post from thread."))
        message = None
        if self.request.POST.get('do') == 'split':
            form = SplitThreadForm(self.request.POST, request=self.request)
            if form.is_valid():
                new_thread = Thread()
                new_thread.forum = form.cleaned_data['thread_forum']
                new_thread.name = form.cleaned_data['thread_name']
                new_thread.slug = slugify(form.cleaned_data['thread_name'])
                new_thread.start = timezone.now()
                new_thread.last = timezone.now()
                new_thread.start_poster_name = 'n'
                new_thread.start_poster_slug = 'n'
                new_thread.last_poster_name = 'n'
                new_thread.last_poster_slug = 'n'
                new_thread.save(force_insert=True)
                for post in self.posts:
                    if post.pk in ids:
                        post.move_to(new_thread)
                        post.save(force_update=True)
                new_thread.sync()
                new_thread.save(force_update=True)
                self.thread.sync()
                self.thread.save(force_update=True)
                self.forum.sync()
                self.forum.save(force_update=True)
                if new_thread.forum != self.forum:
                    new_thread.forum.sync()
                    new_thread.forum.save(force_update=True)
                messages.success(self.request, _("Selected posts have been split to new thread."), 'threads')
                return redirect(reverse(self.type_prefix, kwargs={'thread': new_thread.pk, 'slug': new_thread.slug}))
            message = Message(form.non_field_errors()[0], messages.ERROR)
        else:
            form = SplitThreadForm(request=self.request, initial={
                                                                  'thread_name': _('[Split] %s') % self.thread.name,
                                                                  'thread_forum': self.forum,
                                                                  })
        return render_to_response('%ss/split.html' % self.type_prefix,
                                  {
                                  'type_prefix': self.type_prefix,
                                  'message': message,
                                  'forum': self.forum,
                                  'parents': self.parents,
                                  'thread': self.thread,
                                  'posts': ids,
                                  'form': form,
                                  },
                                  context_instance=RequestContext(self.request));

    def post_action_move(self, ids):
        message = None
        if self.request.POST.get('do') == 'move':
            form = MovePostsForm(self.request.POST, request=self.request, thread=self.thread)
            if form.is_valid():
                thread = form.cleaned_data['thread_url']
                for post in self.posts:
                    if post.pk in ids:
                        post.move_to(thread)
                        post.save(force_update=True)
                if self.thread.post_set.count() == 0:
                    self.thread.delete()
                else:
                    self.thread.sync()
                    self.thread.save(force_update=True)
                thread.sync()
                thread.save(force_update=True)
                thread.forum.sync()
                thread.forum.save(force_update=True)
                if self.forum.pk != thread.forum.pk:
                    self.forum.sync()
                    self.forum.save(force_update=True)
                messages.success(self.request, _("Selected posts have been moved to new thread."), 'threads')
                return redirect(reverse(self.type_prefix, kwargs={'thread': thread.pk, 'slug': thread.slug}))
            message = Message(form.non_field_errors()[0], messages.ERROR)
        else:
            form = MovePostsForm(request=self.request)
        return render_to_response('%ss/move_posts.html' % self.type_prefix,
                                  {
                                  'type_prefix': self.type_prefix,
                                  'message': message,
                                  'forum': self.forum,
                                  'parents': self.parents,
                                  'thread': self.thread,
                                  'posts': ids,
                                  'form': form,
                                  },
                                  context_instance=RequestContext(self.request));

    def post_action_protect(self, ids):
        protected = 0
        for post in self.posts:
            if post.pk in ids and not post.protected:
                protected += 1
        if protected:
            self.thread.post_set.filter(id__in=ids).update(protected=True)
            messages.success(self.request, _('Selected posts have been protected from edition.'), 'threads')
        else:
            messages.info(self.request, _('No posts were protected.'), 'threads')

    def post_action_unprotect(self, ids):
        unprotected = 0
        for post in self.posts:
            if post.pk in ids and post.protected:
                unprotected += 1
        if unprotected:
            self.thread.post_set.filter(id__in=ids).update(protected=False)
            messages.success(self.request, _('Protection from editions has been removed from selected posts.'), 'threads')
        else:
            messages.info(self.request, _('No posts were unprotected.'), 'threads')

    def post_action_undelete(self, ids):
        undeleted = []
        for post in self.posts:
            if post.pk in ids and post.deleted:
                undeleted.append(post.pk)
        if undeleted:
            self.thread.post_set.filter(id__in=undeleted).update(deleted=False, current_date=timezone.now())
            self.thread.sync()
            self.thread.save(force_update=True)
            self.forum.sync()
            self.forum.save(force_update=True)
            messages.success(self.request, _('Selected posts have been restored.'), 'threads')
        else:
            messages.info(self.request, _('No posts were restored.'), 'threads')

    def post_action_soft(self, ids):
        deleted = []
        for post in self.posts:
            if post.pk in ids and not post.deleted:
                if post.pk == self.thread.start_post_id:
                    raise forms.ValidationError(_("You cannot delete first post of thread using this action. If you want to delete thread, use thread moderation instead."))
                deleted.append(post.pk)
        if deleted:
            self.thread.post_set.filter(id__in=deleted).update(deleted=True, current_date=timezone.now(), delete_date=timezone.now())
            self.thread.sync()
            self.thread.save(force_update=True)
            self.forum.sync()
            self.forum.save(force_update=True)
            messages.success(self.request, _('Selected posts have been hidden.'), 'threads')
        else:
            messages.info(self.request, _('No posts were hidden.'), 'threads')

    def post_action_hard(self, ids):
        deleted = []
        for post in self.posts:
            if post.pk in ids:
                if post.pk == self.thread.start_post_id:
                    raise forms.ValidationError(_("You cannot delete first post of thread using this action. If you want to delete thread, use thread moderation instead."))
                deleted.append(post.pk)
        if deleted:
            for post in self.posts:
                if post.pk in deleted:
                    post.delete()
            self.thread.sync()
            self.thread.save(force_update=True)
            self.forum.sync()
            self.forum.save(force_update=True)
            messages.success(self.request, _('Selected posts have been deleted.'), 'threads')
        else:
            messages.info(self.request, _('No posts were deleted.'), 'threads')
