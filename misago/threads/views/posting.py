from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.template import RequestContext
from django.utils import timezone
from django.utils.translation import ugettext as _
from misago.acl.utils import ACLError403, ACLError404
from misago.forms import FormLayout
from misago.forums.models import Forum
from misago.markdown import post_markdown
from misago.messages import Message
from misago.threads.forms import NewThreadForm
from misago.threads.models import Thread, Post
from misago.threads.views.base import BaseView
from misago.views import error403, error404
from misago.utils import slugify

class Posting(BaseView):
    def fetch_forum(self, kwargs):
        self.forum = Forum.objects.get(pk=kwargs['forum'], type='forum')
        self.request.acl.forums.check_forum(self.forum)
        self.request.acl.threads.allow_new_threads(self.forum)
        
    def __call__(self, request, **kwargs):
        self.request = request
        try:
            self.fetch_forum(kwargs)
        except Forum.DoesNotExist:
            return error404(self.request)
        except ACLError403 as e:
            return error403(request, e.message)
        except ACLError404 as e:
            return error404(request, e.message)
        
        message = request.messages.get_message('threads')
        if request.method == 'POST':
            form = NewThreadForm(request.POST, request=request)
            if form.is_valid():
                thread = Thread.objects.create(
                                               forum=self.forum,
                                               name=form.cleaned_data['thread_name'],
                                               slug=slugify(form.cleaned_data['thread_name']),
                                               start=timezone.now(),
                                               last=timezone.now(),
                                               )
                post = Post.objects.create(
                                           forum=self.forum,
                                           thread=thread,
                                           user=request.user,
                                           user_name=request.user.username,
                                           ip=request.session.get_ip(request),
                                           agent=request.META.get('HTTP_USER_AGENT'),
                                           post=form.cleaned_data['post'],
                                           post_preparsed=post_markdown(request, form.cleaned_data['post']),
                                           date=timezone.now()
                                           )
                thread.start_post = post
                thread.last_post = post
                thread.start_poster = request.user
                thread.last_poster = request.user
                thread.start_poster_name = request.user.username
                thread.last_poster_name = request.user.username
                thread.start_poster_slug = request.user.username_slug
                thread.last_poster_slug = request.user.username_slug
                if request.user.rank and request.user.rank.style:
                    thread.start_poster_style = request.user.rank.style
                    thread.last_poster_style = request.user.rank.style
                thread.save(force_update=True)
                
                self.forum.threads += 1
                self.forum.threads_delta += 1
                self.forum.posts += 1
                self.forum.posts_delta += 1
                self.forum.last_thread = thread
                self.forum.last_thread_name = thread.name
                self.forum.last_thread_slug = thread.slug
                self.forum.last_thread_date = thread.last
                self.forum.last_poster = thread.last_poster
                self.forum.last_poster_name = thread.last_poster_name
                self.forum.last_poster_slug = thread.last_poster_slug
                self.forum.last_poster_style = thread.last_poster_style
                self.forum.save(force_update=True)
                
                request.user.topics += 1
                request.user.posts += 1
                request.user.last_post = thread.last
                request.user.save(force_update=True)
                
                request.messages.set_flash(Message(_("New thread has been posted.")), 'success', 'threads')
                return redirect(reverse('forum', kwargs={'forum': self.forum.pk, 'slug': self.forum.slug}))
            message = Message(form.non_field_errors()[0], 'error')
        else:
            form = NewThreadForm(request=request)
        
        return request.theme.render_to_response('threads/posting.html',
                                                {
                                                 'forum': self.forum,
                                                 'message': message,
                                                 'form': FormLayout(form),
                                                 },
                                                context_instance=RequestContext(request));