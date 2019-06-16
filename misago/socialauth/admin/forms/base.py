from django import forms

from ...models import SocialAuthProvider


class ProviderForm(forms.ModelForm):
    class Meta:
        model = SocialAuthProvider
        fields = ["button_text", "button_color", "is_active"]
