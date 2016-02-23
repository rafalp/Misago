from urlparse import urlparse

from django.core.urlresolvers import resolve
from django.http import Http404
from django.utils.translation import ugettext_lazy as _

from misago.acl import add_acl
from misago.categories.forms import CategoryChoiceField
from misago.categories.permissions import (allow_see_category,
                                           allow_browse_category)
from misago.core import forms

from misago.threads.models import Thread
from misago.threads.permissions import allow_see_thread
from misago.threads.validators import validate_title


class MergeThreadsForm(forms.Form):
    merged_thread_title = forms.CharField(label=_("Merged thread title"),
                                          required=False)

    def clean(self):
        data = super(MergeThreadsForm, self).clean()

        merged_thread_title = data.get('merged_thread_title')
        if merged_thread_title:
            validate_title(merged_thread_title)
        else:
            message = _("You have to enter merged thread title.")
            raise forms.ValidationError(message)
        return data


class MoveThreadsForm(forms.Form):
    new_category = CategoryChoiceField(label=_("Move threads to category"),
                                       empty_label=None)

    def __init__(self, *args, **kwargs):
        self.category = kwargs.pop('category')
        acl = kwargs.pop('acl')

        super(MoveThreadsForm, self).__init__(*args, **kwargs)

        self.fields['new_category'].set_acl(acl)

    def clean(self):
        data = super(MoveThreadsForm, self).clean()

        new_category = data.get('new_category')
        if new_category:
            if new_category.is_category:
                message = _("You can't move threads to category.")
                raise forms.ValidationError(message)
            if new_category.is_redirect:
                message = _("You can't move threads to redirect.")
                raise forms.ValidationError(message)
            if new_category.pk == self.category.pk:
                message = _("New category is same as current one.")
                raise forms.ValidationError(message)
        else:
            raise forms.ValidationError(_("You have to select category."))
        return data


class MoveThreadForm(MoveThreadsForm):
    new_category = CategoryChoiceField(label=_("Move thread to category"),
                                       empty_label=None)


class MovePostsForm(forms.Form):
    new_thread_url = forms.CharField(
        label=_("New thread link"),
        help_text=_("Paste link to thread you want selected posts moved to."))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.thread = kwargs.pop('thread')
        self.new_thread = None

        super(MovePostsForm, self).__init__(*args, **kwargs)

    def clean(self):
        data = super(MovePostsForm, self).clean()

        new_thread_url = data.get('new_thread_url')
        try:
            if not new_thread_url:
                raise Http404()

            resolution = resolve(urlparse(new_thread_url).path)
            if not 'thread_id' in resolution.kwargs:
                raise Http404()

            queryset = Thread.objects.select_related('category')
            self.new_thread = queryset.get(id=resolution.kwargs['thread_id'])

            add_acl(self.user, self.new_thread.category)
            add_acl(self.user, self.new_thread)

            allow_see_category(self.user, self.new_thread.category)
            allow_browse_category(self.user, self.new_thread.category)
            allow_see_thread(self.user, self.new_thread)

        except (Http404, Thread.DoesNotExist):
            message = _("You have to enter valid link to thread.")
            raise forms.ValidationError(message)

        if self.thread == self.new_thread:
            message = _("New thread is same as current one.")
            raise forms.ValidationError(message)

        if self.new_thread.category.special_role:
            message = _("You can't move posts to special threads.")
            raise forms.ValidationError(message)

        return data


class SplitThreadForm(forms.Form):
    category = CategoryChoiceField(label=_("New thread category"),
                                 empty_label=None)

    thread_title = forms.CharField(label=_("New thread title"),
                                   required=False)

    def __init__(self, *args, **kwargs):
        acl = kwargs.pop('acl')

        super(SplitThreadForm, self).__init__(*args, **kwargs)

        self.fields['category'].set_acl(acl)

    def clean(self):
        data = super(SplitThreadForm, self).clean()

        category = data.get('category')
        if category:
            if category.is_category:
                message = _("You can't start threads in category.")
                raise forms.ValidationError(message)
            if category.is_redirect:
                message = _("You can't start threads in redirect.")
                raise forms.ValidationError(message)
        else:
            raise forms.ValidationError(_("You have to select category."))

        thread_title = data.get('thread_title')
        if thread_title:
            validate_title(thread_title)
        else:
            message = _("You have to enter new thread title.")
            raise forms.ValidationError(message)

        return data
