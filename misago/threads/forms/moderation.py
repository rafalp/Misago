from django.utils.translation import ugettext_lazy as _

from misago.core import forms
from misago.forums.forms import ForumChoiceField


class MoveThreadsForm(forms.Form):
    new_forum = ForumChoiceField(label=_("Move threads to forum"),
                                 empty_label=None)

    def __init__(self, *args, **kwargs):
        self.forum = kwargs.pop('forum')
        acl = kwargs.pop('acl')

        super(MoveThreadsForm, self).__init__(*args, **kwargs)

        self.fields['new_forum'].set_acl(acl)

    def clean(self):
        data = super(MoveThreadsForm, self).clean()

        new_forum = data.get('new_forum')
        if new_forum:
            if new_forum.is_category:
                message = _("You can't move threads to category.")
                raise forms.ValidationError(message)
            if new_forum.is_redirect:
                message = _("You can't move threads to redirect.")
                raise forms.ValidationError(message)
            if new_forum.pk == self.forum.pk:
                message = _("New forum is same as current one.")
                raise forms.ValidationError(message)
        else:
            raise forms.ValidationError(_("You have to select forum."))
        return data

