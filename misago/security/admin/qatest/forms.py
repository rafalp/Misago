from django.utils.translation import ugettext_lazy as _
from django import forms
from misago.forms import Form

class QATestForm(Form):
    """
    New/Edit QA Test form
    """
    question = forms.CharField(max_length=255)
    helptext = forms.CharField(max_length=255, required=False)
    answers = forms.CharField(widget=forms.Textarea)
    layout = (
               (
                 _("Question and Help"),
                 (
                  ('question', {'label': _("Test Question"), 'help_text': _("Question that is displayed to user.")}),
                  ('helptext', {'label': _("Test Help"), 'help_text': _("Optional help text that is displayed next to question.")}),
                 ),
                ),
                (
                 _("Answers"),
                 (
                  ('answers', {'label': _("Test Answers"), 'help_text': _("Enter accepted answers to this question. Every answer should be entered in new line. Answers are case-insensitive.")}),
                 ),
                ),
               )