from django.template import RequestContext
from django.utils import timezone
from misago.acl.exceptions import ACLError403, ACLError404
from misago.apps.errors import error403, error404
from misago.forms import FormLayout
from misago.markdown import post_markdown
from misago.messages import Message
from misago.models import Forum, Thread, Post, WatchedThread
from misago.utils.translation import ugettext_lazy
from misago.apps.threadtype.base import ViewBase
from misago.apps.threadtype.thread.forms import QuickReplyForm

class PostingBaseView(ViewBase):
    allow_quick_reply = False

    def form_initial_data(self):
        return {}

    def _set_context(self):
        self.set_context()
        if self.forum.level:
            self.parents = Forum.objects.forum_parents(self.forum.pk)

    def record_edit(self, form, old_name, old_post):
        self.post.edits += 1
        self.post.edit_date = timezone.now()
        self.post.edit_user = self.request.user
        self.post.edit_user_name = self.request.user.username
        self.post.edit_user_slug = self.request.user.username_slug
        self.post.save(force_update=True)
        self.post.change_set.create(
                                    forum=self.forum,
                                    thread=self.thread,
                                    post=self.post,
                                    user=self.request.user,
                                    user_name=self.request.user.username,
                                    user_slug=self.request.user.username_slug,
                                    date=self.post.edit_date,
                                    ip=self.request.session.get_ip(self.request),
                                    agent=self.request.META.get('HTTP_USER_AGENT'),
                                    reason=form.cleaned_data['edit_reason'],
                                    size=len(self.post.post),
                                    change=len(self.post.post) - len(old_post),
                                    thread_name_old=old_name if 'thread_name' in form.cleaned_data and form.cleaned_data['thread_name'] != old_name else None,
                                    thread_name_new=self.thread.name if 'thread_name' in form.cleaned_data and form.cleaned_data['thread_name'] != old_name else None,
                                    post_content=old_post,
                                    )

    def after_form(self, form):
        pass

    def email_watchers(self, notified_users):
        pass

    def notify_users(self):
        try:
            post_content = self.md
        except AttributeError:
            post_content = False

        notified_users = []

        if post_content:
            try:
                if (self.quote and self.quote.user_id and
                        self.quote.user.username_slug in post_content.mentions):
                    del post_content.mentions[self.quote.user.username_slug]
                    if not self.quote.user in self.post.mentions.all():
                        notified_users.append(self.quote.user)
                        alert = self.quote.user.alert(ugettext_lazy("%(username)s has replied to your post in thread %(thread)s").message)
                        alert.profile('username', self.request.user)
                        alert.post('thread', self.type_prefix, self.thread, self.post)
                        alert.save_all()
            except KeyError:
                pass
            if post_content.mentions:
                notified_users += [x for x in post_content.mentions.itervalues()]
                self.post.notify_mentioned(self.request, self.type_prefix, post_content.mentions)
                self.post.save(force_update=True)
        self.email_watchers(notified_users)

    def watch_thread(self):
        if self.request.user.subscribe_start:
            try:
                WatchedThread.objects.get(user=self.request.user, thread=self.thread)
            except WatchedThread.DoesNotExist:
                WatchedThread.objects.create(
                                           user=self.request.user,
                                           forum=self.forum,
                                           thread=self.thread,
                                           last_read=timezone.now(),
                                           email=(self.request.user.subscribe_start == 2),
                                           )

    def __call__(self, request, **kwargs):
        self.request = request
        self.kwargs = kwargs
        self.forum = None
        self.thread = None
        self.quote = None
        self.post = None
        self.parents = []
        self.message = request.messages.get_message('threads')

        post_preview = ''
        form = None

        try:
            self._type_available()
            self._set_context()
            self.check_forum_type()
            self._check_permissions()
            if request.method == 'POST':
                # Create correct form instance
                if self.allow_quick_reply and 'quick_reply' in request.POST:
                    form = QuickReplyForm(request.POST, request=request)
                if not form or 'preview' in request.POST or not form.is_valid():
                    # Override "quick reply" form with full one
                    try:
                        form = self.form_type(request.POST, request.FILE, request=request, forum=self.forum, thread=self.thread)
                    except AttributeError:
                        form = self.form_type(request.POST, request=request, forum=self.forum, thread=self.thread)
                
                # Handle specific submit
                if 'preview' in request.POST:
                    form.empty_errors()
                    if form['post'].value():
                        md, post_preview = post_markdown(request, form['post'].value())
                    else:
                        md, post_preview = None, None
                else:
                    if form.is_valid():
                        self.post_form(form)
                        self.watch_thread()
                        self.after_form(form)
                        self.notify_users()
                        return self.response()
                    else:
                        self.message = Message(form.non_field_errors()[0], 'error')
            else:
                form = self.form_type(request=request, forum=self.forum, thread=self.thread, initial=self.form_initial_data())
        except (Forum.DoesNotExist, Thread.DoesNotExist, Post.DoesNotExist):
            return error404(request)
        except ACLError403 as e:
            return error403(request, unicode(e))
        except ACLError404 as e:
            return error404(request, unicode(e))

        return request.theme.render_to_response(('%ss/posting.html' % self.type_prefix),
                                                self.template_vars({
                                                 'type_prefix': self.type_prefix,
                                                 'action': self.action,
                                                 'message': self.message,
                                                 'forum': self.forum,
                                                 'thread': self.thread,
                                                 'quote': self.quote,
                                                 'post': self.post,
                                                 'parents': self.parents,
                                                 'preview': post_preview,
                                                 'form': FormLayout(form),
                                                 }),
                                                context_instance=RequestContext(request));