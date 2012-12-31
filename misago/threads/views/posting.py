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
from misago.threads.forms import PostForm
from misago.threads.models import Thread, Post
from misago.threads.views.base import BaseView
from misago.views import error403, error404
from misago.utils import make_pagination, slugify, ugettext_lazy

class PostingView(BaseView):
    def fetch_target(self, kwargs):
        if self.mode == 'new_thread':
            self.fetch_forum(kwargs)
        if self.mode in ('edit_thread', 'new_post', 'new_post_quick'):
            self.fetch_thread(kwargs)
    
    def fetch_forum(self, kwargs):
        self.forum = Forum.objects.get(pk=kwargs['forum'], type='forum')
        self.request.acl.forums.allow_forum_view(self.forum)
        self.request.acl.threads.allow_new_threads(self.forum)
        self.parents = Forum.objects.forum_parents(self.forum.pk, True)
    
    def fetch_thread(self, kwargs):
        self.thread = Thread.objects.get(pk=kwargs['thread'])
        self.forum = self.thread.forum
        self.request.acl.forums.allow_forum_view(self.forum)
        self.request.acl.threads.allow_thread_view(self.request.user, self.thread)
        self.request.acl.threads.allow_reply(self.thread)
        self.parents = Forum.objects.forum_parents(self.forum.pk, True)
        if kwargs.get('quote'):
            self.quote = Post.objects.select_related('user').get(pk=kwargs['quote'], thread=self.thread.pk)
            self.request.acl.threads.allow_post_view(self.request.user, self.thread, self.quote)
        
    def get_form(self, bound=False):            
        if bound:            
            return PostForm(self.request.POST,request=self.request,mode=self.mode)
        if self.quote:
            quote_post = []
            if self.quote.user:
                quote_post.append('@%s' % self.quote.user.username)
            else:
                quote_post.append('@%s' % self.quote.user_name)
            for line in self.quote.post.splitlines():
                quote_post.append('> %s' % line)
            quote_post.append('\n')
            return PostForm(request=self.request,mode=self.mode,initial={'post': '\n'.join(quote_post)})
        return PostForm(request=self.request,mode=self.mode)
            
    def __call__(self, request, **kwargs):
        self.request = request
        self.forum = None
        self.thread = None
        self.quote = None
        self.post = None
        self.parents = None
        self.mode = kwargs.get('mode')
        if self.request.POST.get('quick_reply') and self.mode == 'new_post':
            self.mode = 'new_post_quick'
        try:
            self.fetch_target(kwargs)
            if not request.user.is_authenticated():
                raise ACLError403(_("Guest, you have to sign-in to post."))
        except (Forum.DoesNotExist, Thread.DoesNotExist, Post.DoesNotExist):
            return error404(self.request)
        except ACLError403 as e:
            return error403(request, e.message)
        except ACLError404 as e:
            return error404(request, e.message)
        
        message = request.messages.get_message('threads')
        if request.method == 'POST':
            form = self.get_form(True)
            if form.is_valid():
                now = timezone.now()
                moderation = False
                if not request.acl.threads.acl[self.forum.pk]['can_approve']:
                    if self.mode == 'new_thread' and request.acl.threads.acl[self.forum.pk]['can_start_threads'] == 1:
                        moderation = True
                    if self.mode in ['new_post', 'new_post_quick'] and request.acl.threads.acl[self.forum.pk]['can_write_posts'] == 1:
                        moderation = True 
                # Get or create new thread
                if self.mode in ['new_thread']:
                    thread = Thread.objects.create(
                                                   forum=self.forum,
                                                   name=form.cleaned_data['thread_name'],
                                                   slug=slugify(form.cleaned_data['thread_name']),
                                                   start=now,
                                                   last=now,
                                                   moderated=moderation,
                                                   score=request.settings['thread_ranking_initial_score'],
                                                   )
                    if moderation:
                        thread.replies_moderated += 1
                else:
                    thread = self.thread
                
                # Create new message
                post = Post.objects.create(
                                           forum=self.forum,
                                           thread=thread,
                                           merge=thread.merges,
                                           user=request.user,
                                           user_name=request.user.username,
                                           ip=request.session.get_ip(request),
                                           agent=request.META.get('HTTP_USER_AGENT'),
                                           post=form.cleaned_data['post'],
                                           post_preparsed=post_markdown(request, form.cleaned_data['post']),
                                           date=now,
                                           moderated=moderation,
                                           )
                
                if self.mode == 'new_thread':
                    thread.start_post = post
                    thread.start_poster = request.user
                    thread.start_poster_name = request.user.username
                    thread.start_poster_slug = request.user.username_slug
                    if request.user.rank and request.user.rank.style:
                        thread.start_poster_style = request.user.rank.style
                
                if self.mode in ['new_post', 'new_post_quick']:
                    if moderation:
                        thread.replies_moderated += 1
                    else:
                        thread.replies += 1
                        if thread.last_poster_id != request.user.pk:
                            thread.score += request.settings['thread_ranking_reply_score']
                        # Notify quoted poster of reply?
                        if self.quote and self.quote.user_id and self.quote.user_id != request.user.pk:
                            alert = self.quote.user.alert(ugettext_lazy("%(username)s has replied to your post in thread %(thread)s.").message)
                            alert.url('username', request.user.username, reverse('user', kwargs={'user': request.user.pk, 'username': request.user.username_slug}))
                            alert.url('thread', self.thread.name, reverse('thread_find', kwargs={'thread': self.thread.pk, 'slug': self.thread.slug, 'post': post.pk}))
                            alert.save_all()
                        if (self.request.settings.thread_length > 0
                            and not thread.closed
                            and thread.replies >= self.request.settings.thread_length):
                            thread.closed = True
                            post.set_checkpoint(self.request, 'limit')
                
                if not moderation:
                    thread.last = now
                    thread.last_post = post
                    thread.last_poster = request.user
                    thread.last_poster_name = request.user.username
                    thread.last_poster_slug = request.user.username_slug
                    if request.user.rank and request.user.rank.style:
                        thread.last_poster_style = request.user.rank.style
                thread.save(force_update=True)
                
                # Update forum and monitor
                if not moderation:
                    if self.mode == 'new_thread':
                        self.request.monitor['threads'] = int(self.request.monitor['threads']) + 1
                        self.forum.threads += 1
                        self.forum.threads_delta += 1
                        
                    if self.mode in ['new_thread', 'new_post', 'new_post_quick']:
                        self.request.monitor['posts'] = int(self.request.monitor['posts']) + 1
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
                
                # Update user
                if not moderation:
                    if self.mode == 'new_thread':
                        request.user.threads += 1
                    request.user.posts += 1
                request.user.last_post = thread.last
                request.user.save(force_update=True)
                
                if self.mode == 'new_thread':
                    if moderation:
                        request.messages.set_flash(Message(_("New thread has been posted. It will be hidden from other members until moderator reviews it.")), 'success', 'threads')
                    else:
                        request.messages.set_flash(Message(_("New thread has been posted.")), 'success', 'threads')
                    return redirect(reverse('thread', kwargs={'thread': thread.pk, 'slug': thread.slug}) + ('#post-%s' % post.pk))
                
                if self.mode in ['new_post', 'new_post_quick']:
                    if moderation:
                        request.messages.set_flash(Message(_("Your reply has been posted. It will be hidden from other members until moderator reviews it.")), 'success', 'threads_%s' % post.pk)
                    else:
                        request.messages.set_flash(Message(_("Your reply has been posted.")), 'success', 'threads_%s' % post.pk)
                    pagination = make_pagination(0, self.request.acl.threads.filter_posts(self.request, self.thread, self.thread.post_set).count(), self.request.settings.posts_per_page)
                    if pagination['total'] > 1:
                        return redirect(reverse('thread', kwargs={'thread': self.thread.pk, 'slug': self.thread.slug, 'page': pagination['total']}) + ('#post-%s' % post.pk))
                    return redirect(reverse('thread', kwargs={'thread': self.thread.pk, 'slug': self.thread.slug}) + ('#post-%s' % post.pk))
            message = Message(form.non_field_errors()[0], 'error')
        else:
            form = self.get_form()
        
        return request.theme.render_to_response('threads/posting.html',
                                                {
                                                 'mode': self.mode,
                                                 'forum': self.forum,
                                                 'thread': self.thread,
                                                 'post': self.post,
                                                 'quote': self.quote,
                                                 'parents': self.parents,
                                                 'message': message,
                                                 'form': FormLayout(form),
                                                 },
                                                context_instance=RequestContext(request));