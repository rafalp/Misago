from django import forms
from django.conf import settings
from django.utils.translation import ungettext, ugettext_lazy as _
from misago.acl.exceptions import ACLError403, ACLError404
from misago.forms import Form, ForumChoiceField
from misago.models import Forum, Thread
from misago.utils.strings import slugify
from misago.validators import validate_sluggable

class ThreadNameMixin(object):
    def clean_thread_name(self):
        data = self.cleaned_data['thread_name']
        slug = slugify(data)
        if len(slug) < self.request.settings['thread_name_min']:
            raise forms.ValidationError(ungettext(
                                                  "Thread name must contain at least one alpha-numeric character.",
                                                  "Thread name must contain at least %(count)d alpha-numeric characters.",
                                                  self.request.settings['thread_name_min']
                                                  ) % {'count': self.request.settings['thread_name_min']})
        if len(data) > self.request.settings['thread_name_max']:
            raise forms.ValidationError(ungettext(
                                                  "Thread name cannot be longer than %(count)d character.",
                                                  "Thread name cannot be longer than %(count)d characters.",
                                                  self.request.settings['thread_name_max']
                                                  ) % {'count': self.request.settings['thread_name_max']})
        return data


class PostForm(Form, ThreadNameMixin):
    post = forms.CharField(widget=forms.Textarea)

    def __init__(self, data=None, file=None, request=None, mode=None, *args, **kwargs):
        self.mode = mode
        super(PostForm, self).__init__(data, file, request=request, *args, **kwargs)

    def finalize_form(self):
        self.layout = [
                       [
                        None,
                        [
                         ('thread_name', {'label': _("Thread Name")}),
                         ('edit_reason', {'label': _("Edit Reason")}),
                         ('post', {'label': _("Post Content")}),
                         ],
                        ],
                       ]

        if self.mode in ['edit_thread', 'edit_post']:
            self.fields['edit_reason'] = forms.CharField(max_length=255, required=False, help_text=_("Optional reason for changing this post."))
        else:
            del self.layout[0][1][1]

        if self.mode not in ['edit_thread', 'new_thread']:
            del self.layout[0][1][0]
        else:
            self.fields['thread_name'] = forms.CharField(
                                                         max_length=self.request.settings['thread_name_max'],
                                                         validators=[validate_sluggable(
                                                                                        _("Thread name must contain at least one alpha-numeric character."),
                                                                                        _("Thread name is too long. Try shorter name.")
                                                                                        )])

    def clean_post(self):
        data = self.cleaned_data['post']
        if len(data) < self.request.settings['post_length_min']:
            raise forms.ValidationError(ungettext(
                                                  "Post content cannot be empty.",
                                                  "Post content cannot be shorter than %(count)d characters.",
                                                  self.request.settings['post_length_min']
                                                  ) % {'count': self.request.settings['post_length_min']})
        return data



class SplitThreadForm(Form, ThreadNameMixin):
    def finalize_form(self):
        self.layout = [
                       [
                        None,
                        [
                         ('thread_name', {'label': _("New Thread Name")}),
                         ('thread_forum', {'label': _("New Thread Forum")}),
                         ],
                        ],
                       ]

        self.fields['thread_name'] = forms.CharField(
                                                     max_length=self.request.settings['thread_name_max'],
                                                     validators=[validate_sluggable(
                                                                                    _("Thread name must contain at least one alpha-numeric character."),
                                                                                    _("Thread name is too long. Try shorter name.")
                                                                                    )])
        self.fields['thread_forum'] = ForumChoiceField(queryset=Forum.tree.get(token='root').get_descendants().filter(pk__in=self.request.acl.forums.acl['can_browse']))

    def clean_thread_forum(self):
        new_forum = self.cleaned_data['thread_forum']
        # Assert its forum and its not current forum
        if new_forum.type != 'forum':
            raise forms.ValidationError(_("This is not a forum."))
        return new_forum


class MovePostsForm(Form, ThreadNameMixin):
    error_source = 'thread_url'

    def __init__(self, data=None, request=None, thread=None, *args, **kwargs):
        self.thread = thread
        super(MovePostsForm, self).__init__(data, request=request, *args, **kwargs)

    def finalize_form(self):
        self.layout = [
                       [
                        None,
                        [
                         ('thread_url', {'label': _("New Thread Link"), 'help_text': _("To select new thread, simply copy and paste here its link.")}),
                         ],
                        ],
                       ]

        self.fields['thread_url'] = forms.CharField()

    def clean_thread_url(self):
        from django.core.urlresolvers import resolve
        from django.http import Http404
        thread_url = self.cleaned_data['thread_url']
        try:
            thread_url = thread_url[len(settings.BOARD_ADDRESS):]
            match = resolve(thread_url)
            thread = Thread.objects.get(pk=match.kwargs['thread'])
            self.request.acl.threads.allow_thread_view(self.request.user, thread)
            if thread.pk == self.thread.pk:
                raise forms.ValidationError(_("New thread is same as current one."))
            return thread
        except (Http404, KeyError):
            raise forms.ValidationError(_("This is not a correct thread URL."))
        except (Thread.DoesNotExist, ACLError403, ACLError404):
            raise forms.ValidationError(_("Thread could not be found."))


class QuickReplyForm(Form):
    post = forms.CharField(widget=forms.Textarea)


class MoveThreadsForm(Form):
    error_source = 'new_forum'

    def __init__(self, data=None, request=None, forum=None, *args, **kwargs):
        self.forum = forum
        super(MoveThreadsForm, self).__init__(data, request=request, *args, **kwargs)

    def finalize_form(self):
        self.fields['new_forum'] = ForumChoiceField(queryset=Forum.tree.get(token='root').get_descendants().filter(pk__in=self.request.acl.forums.acl['can_browse']))
        self.layout = [
                       [
                        None,
                        [
                         ('new_forum', {'label': _("Move Threads to"), 'help_text': _("Select forum you want to move threads to.")}),
                         ],
                        ],
                       ]

    def clean_new_forum(self):
        new_forum = self.cleaned_data['new_forum']
        # Assert its forum and its not current forum
        if new_forum.type != 'forum':
            raise forms.ValidationError(_("This is not forum."))
        if new_forum.pk == self.forum.pk:
            raise forms.ValidationError(_("New forum is same as current one."))
        return new_forum


class MergeThreadsForm(Form, ThreadNameMixin):
    def __init__(self, data=None, request=None, threads=[], *args, **kwargs):
        self.threads = threads
        super(MergeThreadsForm, self).__init__(data, request=request, *args, **kwargs)

    def finalize_form(self):
        self.fields['new_forum'] = ForumChoiceField(queryset=Forum.tree.get(token='root').get_descendants().filter(pk__in=self.request.acl.forums.acl['can_browse']), initial=self.threads[0].forum)
        self.fields['thread_name'] = forms.CharField(
                                                     max_length=self.request.settings['thread_name_max'],
                                                     initial=self.threads[0].name,
                                                     validators=[validate_sluggable(
                                                                                    _("Thread name must contain at least one alpha-numeric character."),
                                                                                    _("Thread name is too long. Try shorter name.")
                                                                                    )])
        self.layout = [
                       [
                        None,
                        [
                         ('thread_name', {'label': _("Thread Name"), 'help_text': _("Name of new thread that will be created as result of merge.")}),
                         ('new_forum', {'label': _("Thread Forum"), 'help_text': _("Select forum you want to put new thread in.")}),
                         ],
                        ],
                       [
                        _("Merge Order"),
                        [
                         ],
                        ],
                       ]

        choices = []
        for i, thread in enumerate(self.threads):
            choices.append((str(i), i + 1))
        for i, thread in enumerate(self.threads):
            self.fields['thread_%s' % thread.pk] = forms.ChoiceField(choices=choices, initial=str(i))
            self.layout[1][1].append(('thread_%s' % thread.pk, {'label': thread.name}))

    def clean_new_forum(self):
        new_forum = self.cleaned_data['new_forum']
        # Assert its forum
        if new_forum.type != 'forum':
            raise forms.ValidationError(_("This is not forum."))
        return new_forum

    def clean(self):
        cleaned_data = super(MergeThreadsForm, self).clean()
        self.merge_order = {}
        lookback = []
        for thread in self.threads:
            order = int(cleaned_data['thread_%s' % thread.pk])
            if order in lookback:
                raise forms.ValidationError(_("One or more threads have same position in merge order."))
            lookback.append(order)
            self.merge_order[order] = thread
        return cleaned_data
