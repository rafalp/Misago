from django import forms
from django.utils.translation import ugettext_lazy as _
from misago.apps.threadtype.mixins import ValidateThreadNameMixin
from misago.forms import Form
from misago.validators import validate_sluggable

class PostingForm(Form):
    post = forms.CharField(widget=forms.Textarea)

    def __init__(self, data=None, file=None, request=None, forum=None, thread=None, *args, **kwargs):
        self.forum = forum
        self.thread = thread
        super(PostingForm, self).__init__(data, file, request=request, *args, **kwargs)

    def set_extra_fields(self):
        # Can we change threads states?
        if self.request.acl.threads.can_pin_threads(self.forum):
            thread_weight = []
            if (not self.thread or self.thread.weight < 2) and self.request.acl.threads.can_pin_threads(self.forum) == 2:
                thread_weight.append((2, _("Announcement")))
            if (not self.thread or self.thread.weight == 0) and self.request.acl.threads.can_pin_threads(self.forum):
                thread_weight.append((1, _("Sticky")))
            if (not self.thread or self.thread.weight != 0):
                thread_weight.append((0, _("Standard")))
            if thread_weight:
                self.layout[0][1].append(('thread_weight', {'label': _("Thread Importance")}))
                self.fields['thread_weight'] = forms.TypedChoiceField(widget=forms.RadioSelect, choices=thread_weight, coerce=int, initial=0)

        # Can we lock threads?
        if self.request.acl.threads.can_close(self.forum):
            self.fields['close_thread'] = forms.BooleanField(required=False)
            if self.thread and self.thread.closed:
                self.layout[0][1].append(('close_thread', {'label': 'NOEZ', 'inline': _("Open Thread")}))
            else:
                self.layout[0][1].append(('close_thread', {'label': 'BALLS', 'inline': _("Close Thread")}))


class NewThreadForm(PostingForm, ValidateThreadNameMixin):
    def finalize_form(self):
        self.layout = [
                       [
                        None,
                        [
                         ('thread_name', {'label': _("Thread Name")}),
                         ('post', {'label': _("Post Content")}),
                         ]
                        ]
                       ]

        self.fields['thread_name'] = forms.CharField(max_length=self.request.settings['thread_name_max'],
                                                     validators=[validate_sluggable(_("Thread name must contain at least one alpha-numeric character."),
                                                                                    _("Thread name is too long. Try shorter name."))])

        self.set_extra_fields()
