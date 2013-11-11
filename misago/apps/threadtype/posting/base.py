from django.template import RequestContext
from django.utils import timezone
from django.utils.translation import ugettext as _
from floppyforms import ValidationError
from misago import messages
from misago.acl.exceptions import ACLError403, ACLError404
from misago.apps.errors import error403, error404
from misago.markdown import emojis, post_markdown
from misago.messages import Message
from misago.models import Attachment, AttachmentType, Forum, Thread, Post, WatchedThread
from misago.shortcuts import render_to_response
from misago.utils.translation import ugettext_lazy
from misago.apps.threadtype.base import ViewBase
from misago.apps.threadtype.thread.forms import QuickReplyForm

class PostingBaseView(ViewBase):
    allow_quick_reply = False
    block_flood_requests = True

    def form_initial_data(self):
        return {}

    def _set_context(self):
        self.set_context()
        if self.forum.level:
            self.parents = Forum.objects.forum_parents(self.forum.pk)

    def record_edit(self, form, old_name, old_post):
        self.post.edits += 1
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
                                    date=self.post.current_date,
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
            post_mentions = self.md.mentions
        except AttributeError:
            post_mentions = False

        notified_users = []

        if post_mentions:
            try:
                if (self.quote and self.quote.user_id and
                        self.quote.user.username_slug in post_mentions):
                    del post_mentions[self.quote.user.username_slug]
                    if not self.quote.user in self.post.mentions.all():
                        notified_users.append(self.quote.user)
                        self.post.mentions.add(self.quote.user)
                        alert = self.quote.user.alert(ugettext_lazy("%(username)s has replied to your post in thread %(thread)s").message)
                        alert.profile('username', self.request.user)
                        alert.post('thread', self.type_prefix, self.thread, self.post)
                        alert.save_all()
            except KeyError:
                pass
            if post_mentions:
                notified_users += [x for x in post_mentions.values()]
                self.post.notify_mentioned(self.request, self.type_prefix, post_mentions)
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
                                           starter_id=self.thread.start_poster_id,
                                           last_read=timezone.now(),
                                           email=(self.request.user.subscribe_start == 2),
                                           )

    def make_attachments_token(self):
        if self.post_id:
            self.attachments_token = 'attachments_%s' % self.post_id
        else:
            forum_pk = self.forum.pk
            try:
                thread_pk = self.thread.id
            except AttributeError:
                thread_pk = 0
            self.attachments_token = 'attachments_%s_%s_%s' % (self.request.user.pk, forum_pk, thread_pk)
        self.attachments_removed_token = 'removed_%s' % self.attachments_token

    def session_attachments_queryset(self):
        session_pks = self.request.session.get(self.attachments_token, 'nada')
        if session_pks == 'nada':
            session_pks = [a.pk for a in Attachment.objects.filter(session=self.attachments_token).iterator()]
            self.request.session[self.attachments_token] = session_pks

        self.session_attachments = session_pks
        return Attachment.objects.filter(id__in=session_pks).order_by('-id').iterator()

    def fetch_removed_attachments(self):
        self.attachments_removed = self.request.session.get(self.attachments_removed_token, 'nada')
        if self.attachments_removed == 'nada':
            self.attachments_removed = []
            self.request.session[self.attachments_removed_token] = []

    def fetch_attachments(self):
        self.attachments = []
        self.user_attachments = 0

        self.attachments_removed = []
        self.fetch_removed_attachments()

        for attachment in self.session_attachments_queryset():
            self.attachments.append(attachment)
            if attachment.user_id == self.request.user.pk and not attachment.pk in self.attachments_removed:
                self.user_attachments += 1

    def _upload_file(self, uploaded_file):
        try:
            self.request.acl.threads.allow_upload_attachments(self.forum)
            attachments_limit = self.request.acl.threads.attachments_limit(self.forum)
            if attachments_limit != 0 and self.user_attachments >= attachments_limit:
                raise ACLError403(_("You can't attach any more files to this form."))

            if not uploaded_file:
                raise ValidationError(_("You have to upload file."))

            Attachment.objects.allow_more_orphans()

            attachment_type = AttachmentType.objects.find_type(uploaded_file.name)
            if not attachment_type:
                raise ValidationError(_("This is not an allowed file type."))
            attachment_type.allow_file_upload(self.request.user,
                                              self.request.acl.threads.attachment_size_limit(self.forum),
                                              uploaded_file.size)

            new_attachment = Attachment()
            new_attachment.generate_hash_id(self.attachments_token)
            new_attachment.session = self.attachments_token
            new_attachment.filetype = attachment_type
            new_attachment.user = self.request.user
            new_attachment.user_name = self.request.user.username
            new_attachment.user_name_slug = self.request.user.username_slug
            new_attachment.ip = self.request.session.get_ip(self.request)
            new_attachment.agent = self.request.META.get('HTTP_USER_AGENT')
            new_attachment.use_file(uploaded_file)
            new_attachment.save(force_insert=True)

            self.session_attachments.append(new_attachment.pk)
            self.request.session[self.attachments_token] = self.session_attachments
            self.attachments.insert(0, new_attachment)
            self.message = Message(_('File "%(filename)s" has been attached successfully.') % {'filename': new_attachment.name})
        except ACLError403 as e:
            self.message = Message(unicode(e), messages.ERROR)
        except ValidationError as e:
            self.message = Message(unicode(e.messages[0]), messages.ERROR)

    def remove_attachment(self, attachment_pk):
        try:
            index = None
            attachment = None
            for index, attachment in enumerate(self.attachments):
                if attachment.pk == attachment_pk:
                    break
            else:
                raise ValidationError(_('Requested attachment could not be found.'))
            self.request.acl.threads.allow_attachment_delete(self.request.user, self.forum, attachment)

            if not attachment.pk in self.attachments_removed:
                self.attachments_removed.append(attachment.pk)
                self.request.session[self.attachments_removed_token] = self.attachments_removed
                self.message = Message(_('File "%(filename)s" has been removed.') % {'filename': attachment.name})
        except ACLError403 as e:
            self.message = Message(unicode(e), messages.ERROR)
        except ValidationError as e:
            self.message = Message(unicode(e.messages[0]), messages.ERROR)

    def restore_attachment(self, attachment_pk):
        try:
            index = None
            attachment = None
            for index, attachment in enumerate(self.attachments):
                if attachment.pk == attachment_pk:
                    break
            else:
                raise ValidationError(_('Requested attachment could not be found.'))

            if attachment.pk in self.attachments_removed:
                self.attachments_removed.remove(attachment.pk)
                self.request.session[self.attachments_removed_token] = self.attachments_removed
                self.message = Message(_('File "%(filename)s" has been restored.') % {'filename': attachment.name})
        except ACLError403 as e:
            self.message = Message(unicode(e), messages.ERROR)
        except ValidationError as e:
            self.message = Message(unicode(e.messages[0]), messages.ERROR)

    def finalize_attachments(self):
        del self.request.session[self.attachments_token]
        del self.request.session[self.attachments_removed_token]
        self.make_attachments_token()

        post_attachments = []
        for attachment in self.attachments:
            if attachment.pk in self.attachments_removed:
                attachment.delete()
            else:
                post_attachments.append(attachment)
                attachment.forum = self.forum
                attachment.thread = self.thread
                attachment.post = self.post
                attachment.session = self.attachments_token
                attachment.save()

        if self.post.has_attachments or post_attachments:
            self.post.attachments = post_attachments
            self.post.save(force_update=True)

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
            request.block_flood_requests = self.block_flood_requests
            self.make_attachments_token()
            self.fetch_attachments()
            if request.method == 'POST':
                # Create correct form instance
                if self.allow_quick_reply and 'quick_reply' in request.POST:
                    form = QuickReplyForm(request.POST, request=request)
                if not form or 'preview' in request.POST or not form.is_valid():
                    # Override "quick reply" form with full one
                    try:
                        form = self.form_type(request.POST, request.FILES, request=request, forum=self.forum, thread=self.thread)
                    except AttributeError:
                        form = self.form_type(request.POST, request=request, forum=self.forum, thread=self.thread)
                # Handle specific submit
                if list(set(request.POST.keys()) & set(('preview', 'upload', 'remove_attachment', 'restore_attachment'))):
                    form.empty_errors()
                    if form['post'].value():
                        md, post_preview = post_markdown(form['post'].value())
                    else:
                        md, post_preview = None, None
                    if 'upload' in request.POST:
                        try:
                            uploaded_file = form['new_file'].value()
                        except KeyError:
                            uploaded_file = None
                        self._upload_file(uploaded_file)
                    if 'remove_attachment' in request.POST:
                        try:
                            self.remove_attachment(int(request.POST.get('remove_attachment')))
                        except ValueError:
                            self.message = Message(_("Requested attachment could not be found."), messages.ERROR)
                    if 'restore_attachment' in request.POST:
                        try:
                            self.restore_attachment(int(request.POST.get('restore_attachment')))
                        except ValueError:
                            self.message = Message(_("Requested attachment could not be found."), messages.ERROR)
                else:
                    if form.is_valid():
                        self.post_form(form)
                        self.watch_thread()
                        self.after_form(form)
                        self.finalize_attachments()
                        self.notify_users()
                        return self.response()
                    else:
                        self.message = Message(form.non_field_errors()[0], messages.ERROR)
            else:
                form = self.form_type(request=request, forum=self.forum, thread=self.thread, initial=self.form_initial_data())
        except (Forum.DoesNotExist, Thread.DoesNotExist, Post.DoesNotExist):
            return error404(request)
        except ACLError403 as e:
            return error403(request, unicode(e))
        except ACLError404 as e:
            return error404(request, unicode(e))

        return render_to_response('%ss/posting.html' % self.type_prefix,
                                  self._template_vars({
                                        'action': self.action,
                                        'attachments': self.attachments,
                                        'attachments_types': AttachmentType.objects.all_types(),
                                        'attachments_removed': self.attachments_removed,
                                        'attachments_number': self.user_attachments,
                                        'message': self.message,
                                        'forum': self.forum,
                                        'thread': self.thread,
                                        'quote': self.quote,
                                        'post': self.post,
                                        'parents': self.parents,
                                        'preview': post_preview,
                                        'form': form,
                                        'emojis': emojis(),
                                      }),
                                  context_instance=RequestContext(request));
