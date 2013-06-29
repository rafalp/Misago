from django import forms
from django.utils.translation import ugettext_lazy as _
from misago.conf import settings
from misago.forms import Form, ForumChoiceField
from misago.models import Forum
from misago.validators import validate_sluggable
from misago.apps.threadtype.mixins import ValidateThreadNameMixin

class MoveThreadsForm(Form):
    error_source = 'new_forum'

    def __init__(self, data=None, request=None, forum=None, *args, **kwargs):
        self.forum = forum
        super(MoveThreadsForm, self).__init__(data, request=request, *args, **kwargs)

    def finalize_form(self):
        self.fields['new_forum'] = ForumChoiceField(queryset=Forum.objects.get(special='root').get_descendants().filter(pk__in=self.request.acl.forums.acl['can_browse']))
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


class MergeThreadsForm(Form, ValidateThreadNameMixin):
    def __init__(self, data=None, request=None, threads=[], *args, **kwargs):
        self.threads = threads
        super(MergeThreadsForm, self).__init__(data, request=request, *args, **kwargs)

    def finalize_form(self):
        self.fields['new_forum'] = ForumChoiceField(queryset=Forum.objects.get(special='root').get_descendants().filter(pk__in=self.request.acl.forums.acl['can_browse']), initial=self.threads[0].forum)
        self.fields['thread_name'] = forms.CharField(
                                                     max_length=settings.thread_name_max,
                                                     initial=self.threads[-1].name,
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
                       ]

    def clean_new_forum(self):
        new_forum = self.cleaned_data['new_forum']
        if new_forum.type != 'forum':
            raise forms.ValidationError(_("This is not forum."))
        return new_forum
