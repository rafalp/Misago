from django import forms

from ..states.start import StartState


class StartForm(forms.Form):
    title = forms.CharField(max_length=200)
    post = forms.CharField(max_length=2000, widget=forms.Textarea)

    def update_state(self, state: StartState):
        state.set_thread_title(self.cleaned_data["title"])
        state.set_post_message(self.cleaned_data["post"])


class ThreadStartForm(StartForm):
    pass
