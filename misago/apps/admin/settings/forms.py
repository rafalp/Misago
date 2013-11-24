from django import forms
from misago.forms import Form

class SearchForm(Form):
    search_text = forms.CharField(max_length=255)
