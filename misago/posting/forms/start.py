from django import forms


class StartForm(forms.Form):
    title = forms.CharField(max_length=200)
    post = forms.CharField(max_length=2000, widget=forms.Textarea)


class ThreadStartForm(StartForm):
    pass
