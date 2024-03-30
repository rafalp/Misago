from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class AccountPreferencesForm(forms.ModelForm):
    is_hiding_presence = forms.TypedChoiceField(
        coerce=int,
        choices=(
            (1, "Show me to everyone"),
            (0, "Show me to nobody"),
        ),
    )

    class Meta:
        model = User
        fields = [
            "is_hiding_presence",
        ]
