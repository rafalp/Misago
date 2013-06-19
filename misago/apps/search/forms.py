from django import forms
from django.utils import timezone
from django.utils.translation import ungettext_lazy, ugettext_lazy as _
from misago.forms import Form

class QuickSearchForm(Form):
    search_query = forms.CharField(max_length=255)

    def clean_search_query(self):
        data = self.cleaned_data['search_query']
        if len(data) < 3:
            raise forms.ValidationError(_("Search query should be at least 3 characters long."))

        self.mode = None

        if data[0:6].lower() == 'forum:':
            forum_name = data[6:].strip()
            if len(forum_name) < 2:
                raise forms.ValidationError(_("In order to jump to forum, You have to enter full forum name or first few characters of it."))
            self.mode = 'forum'
            self.target = forum_name

        if data[0:5].lower() == 'user:':
            username = data[5:].strip()
            if len(username) < 2:
                raise forms.ValidationError(_("In order to jump to user profile, You have to enter full user name or first few characters of it."))
            self.mode = 'user'
            self.target = username

        return data

    def clean(self):
        cleaned_data = super(QuickSearchForm, self).clean()
        if self.request.user.last_search:
            diff = timezone.now() - self.request.user.last_search
            diff = diff.seconds + (diff.days * 86400)
            wait_for = self.request.acl.search.search_cooldown() - diff
            if wait_for > 0:
                if wait_for < 5:
                    raise forms.ValidationError(_("You can't perform one search so quickly after another. Please wait a moment and try again."))
                else:
                    raise forms.ValidationError(ungettext(
                            "You can't perform one search so quickly after another. Please wait %(seconds)d second and try again.",
                            "You can't perform one search so quickly after another. Please wait %(seconds)d seconds and try again.",
                        wait_for) % {
                            'seconds': wait_for,
                        })
        return cleaned_data
