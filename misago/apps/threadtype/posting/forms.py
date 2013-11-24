from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
import floppyforms as forms
from misago.apps.threadtype.mixins import (FloodProtectionMixin,
                                           ValidateThreadNameMixin,
                                           ValidatePostLengthMixin)
from misago.conf import settings
from misago.forms import Form
from misago.validators import validate_sluggable

class PostingForm(FloodProtectionMixin, Form, ValidatePostLengthMixin):
    include_thread_weight = True
    include_close_thread = True
    post = forms.CharField(label=_("Message Body"), widget=forms.Textarea)

    def __init__(self, data=None, file=None, request=None, forum=None, thread=None, *args, **kwargs):
        self.forum = forum
        self.thread = thread
        if data and thread:
            data = data.copy()
            if not 'thread_weight' in data:
                data['thread_weight'] = thread.weight
        super(PostingForm, self).__init__(data, file, request=request, *args, **kwargs)

    def finalize_form(self):
        # Can we change threads states?
        if self.include_thread_weight and (self.request.acl.threads.can_pin_threads(self.forum) and
            (not self.thread or self.request.acl.threads.can_pin_threads(self.forum) >= self.thread.weight)):
            thread_weight = []
            if self.request.acl.threads.can_pin_threads(self.forum) == 2:
                thread_weight.append((2, _("Announcement")))
            thread_weight.append((1, _("Sticky")))
            thread_weight.append((0, _("Standard")))
            if thread_weight:
                try:
                    current_weight = self.thread.weight
                except AttributeError:
                    current_weight = 0
                self.add_field('thread_weight', forms.TypedChoiceField(widget=forms.RadioSelect,
                                                                       choices=thread_weight,
                                                                       required=False,
                                                                       coerce=int,
                                                                       initial=current_weight))

        # Can we lock threads?
        if self.include_close_thread and self.request.acl.threads.can_close(self.forum):
            self.add_field('close_thread', forms.BooleanField(required=False))

        if self.request.acl.threads.can_upload_attachments(self.forum):
            self.add_field('new_file', forms.FileField(required=False))

        # Give inheritor chance to set custom fields
        try:
            type_fields_call = self.type_fields
        except AttributeError:
            type_fields_call = None
        if type_fields_call:
            type_fields_call()

    def clean_thread_weight(self):
        data = self.cleaned_data['thread_weight']
        if not data:
            try:
                return self.thread.weight
            except AttributeError:
                pass
            return 0
        return data


class NewThreadForm(PostingForm, ValidateThreadNameMixin):
    def finalize_form(self):
        super(NewThreadForm, self).finalize_form()
        self.add_field('thread_name', forms.CharField(label=_("Thread Name"),
                                                      max_length=settings.thread_name_max,
                                                      validators=[validate_sluggable(_("Thread name must contain at least one alpha-numeric character."),
                                                                                     _("Thread name is too long. Try shorter name."))]))


class EditThreadForm(NewThreadForm, ValidateThreadNameMixin):
    def finalize_form(self):
        super(EditThreadForm, self).finalize_form()
        self.add_field('edit_reason', forms.CharField(label=_("Edit Reason"),
                                                      help_text=_("Optional reason for editing this thread."),
                                                      max_length=255,
                                                      required=False))


class NewReplyForm(PostingForm):
    pass


class EditReplyForm(PostingForm):
    def finalize_form(self):
        super(EditReplyForm, self).finalize_form()
        self.add_field('edit_reason', forms.CharField(label=_("Edit Reason"),
                                                      help_text=_("Optional reason for editing this reply."),
                                                      max_length=255,
                                                      required=False))
