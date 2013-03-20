from django.template import RequestContext
from django.utils import timezone
from misago.acl.exceptions import ACLError403, ACLError404
from misago.apps.errors import error403, error404
from misago.forms import FormLayout
from misago.markdown import post_markdown
from misago.messages import Message
from misago.models import Forum, WatchedThread
from misago.apps.threadtype.base import ViewBase

class PostingBaseView(ViewBase):
    def form_initial_data(self):
        return {}

    def _set_context(self):
        self.set_context()
        if self.forum.level:
            self.parents = Forum.objects.forum_parents(self.forum.pk)

    def record_edit(self, form, old_name, old_post):
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
                                    thread_name_old=old_name if form.cleaned_data['thread_name'] != old_name else None,
                                    thread_name_new=self.thread.name if form.cleaned_data['thread_name'] != old_name else None,
                                    post_content=old_post,
                                    )

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

        try:
            self._set_context()
            if request.method == 'POST':
                try:
                    form = self.form_type(request.POST, request.FILE, request=request, forum=self.forum, thread=self.thread)
                except AttributeError:
                    form = self.form_type(request.POST, request=request, forum=self.forum, thread=self.thread)

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
                        return self.response()
                    else:
                        message = Message(form.non_field_errors()[0], 'error')
            else:
                form = self.form_type(request=request, forum=self.forum, thread=self.thread, initial=self.form_initial_data())
        except Forum.DoesNotExist:
            return error404(request)
        except ACLError403 as e:
            return error403(request, unicode(e))
        except ACLError404 as e:
            return error404(request, unicode(e))

        return request.theme.render_to_response(('%s/posting.html' % self.templates_prefix),
                                                {
                                                 'action': self.action,
                                                 'message': self.message,
                                                 'forum': self.forum,
                                                 'thread': self.thread,
                                                 'quote': self.quote,
                                                 'post': self.post,
                                                 'parents': self.parents,
                                                 'preview': post_preview,
                                                 'form': FormLayout(form),
                                                 },
                                                context_instance=RequestContext(request));