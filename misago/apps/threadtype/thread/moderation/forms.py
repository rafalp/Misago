from django.http import Http404
from django.utils.translation import ugettext_lazy as _
import floppyforms as forms
from misago.acl.exceptions import ACLError403, ACLError404
from misago.conf import settings
from misago.forms import Form, ForumChoiceField
from misago.models import Forum, Thread
from misago.validators import validate_sluggable
from misago.apps.threadtype.mixins import ValidateThreadNameMixin

class SplitThreadForm(Form, ValidateThreadNameMixin):
    def finalize_form(self):
        self.fields['thread_name'] = forms.CharField(label=_("New Thread Name"),
                                                     max_length=settings.thread_name_max,
                                                     validators=[validate_sluggable(_("Thread name must contain at least one alpha-numeric character."),
                                                                                    _("Thread name is too long. Try shorter name.")
                                                                                    )])
        self.fields['thread_forum'] = ForumChoiceField(label=_("New Thread Forum"),
                                                       queryset=Forum.objects.get(special='root').get_descendants().filter(pk__in=self.request.acl.forums.acl['can_browse']))

    def clean_thread_forum(self):
        new_forum = self.cleaned_data['thread_forum']
        # Assert its forum and its not current forum
        if new_forum.type != 'forum':
            raise forms.ValidationError(_("This is not a forum."))
        return new_forum


def get_thread_from_url(request, thread_url):
        from django.core.urlresolvers import resolve
        from django.http import Http404

        try:
            thread_url = thread_url[len(settings.BOARD_ADDRESS):]
            match = resolve(thread_url)
            if not match.url_name.startswith('thread'):
                raise forms.ValidationError(_("This is not a correct thread URL."))
            thread = Thread.objects.get(pk=match.kwargs['thread'])
            request.acl.threads.allow_thread_view(request.user, thread)
            if thread.pk == self.thread.pk:
                raise forms.ValidationError(_("New thread is same as current one."))
            return thread
        except (Http404, KeyError):
            raise forms.ValidationError(_("This is not a correct thread URL."))
        except (Thread.DoesNotExist, ACLError403, ACLError404):
            raise forms.ValidationError(_("Thread could not be found."))


class MovePostsForm(Form, ValidateThreadNameMixin):
    error_source = 'thread_url'

    def __init__(self, data=None, request=None, thread=None, *args, **kwargs):
        self.thread = thread
        super(MovePostsForm, self).__init__(data, request=request, *args, **kwargs)

    def finalize_form(self):
        self.fields['thread_url'] = forms.CharField(label=_("New Thread Link"),
                                                    help_text=_("To select new thread, simply copy and paste here its link."))

    def clean_thread_url(self):
        return get_thread_from_url(
            self.request, self.cleaned_data['thread_url'])
