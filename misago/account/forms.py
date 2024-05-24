from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import pgettext_lazy

User = get_user_model()


class AccountPreferencesForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "limits_private_thread_invites_to",
            "watch_started_threads",
            "watch_replied_threads",
            "watch_new_private_threads_by_followed",
            "watch_new_private_threads_by_other_users",
            "notify_new_private_threads_by_followed",
            "notify_new_private_threads_by_other_users",
        ]
        widgets = {
            "limits_private_thread_invites_to": forms.RadioSelect(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        user = kwargs["instance"]

        self.fields["is_hiding_presence"] = forms.TypedChoiceField(
            coerce=int,
            choices=(
                (
                    1,
                    pgettext_lazy(
                        "account privacy choice",
                        "Show other users when I am online",
                    ),
                ),
                (
                    0,
                    pgettext_lazy(
                        "account privacy choice",
                        "Don't show other users when I am online",
                    ),
                ),
            ),
            initial=0 if user.is_hiding_presence else 1,
            widget=forms.RadioSelect(),
        )

    def save(self):
        self.instance.is_hiding_presence = not self.cleaned_data.get(
            "is_hiding_presence"
        )
        return super().save()
