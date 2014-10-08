from django.utils.translation import ugettext_lazy as _

from misago.core import forms
from misago.forums.forms import ForumChoiceField


class MoveThreadsBaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.forum = kwargs.pop('forum')
        super(MoveThreadsBaseForm, self).__init__(*args, **kwargs)

    def clean(self):
        data = super(MoveThreadsBaseForm, self).clean()

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


def MoveThreadsForm(*args, **kwargs):
    user = kwargs.pop('user')
    label = kwargs.pop('label', _("Move threads to forum"))
    forum_field = ForumChoiceField(label=label, acl=user.acl, empty_label=None)

    FormType = type("FinalMoveThreadsForm", (MoveThreadsBaseForm,), {
        'new_forum': forum_field,
    })
    return FormType(*args, **kwargs)
