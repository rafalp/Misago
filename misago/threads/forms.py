from django import forms
from django.utils.translation import ugettext_lazy as _
from misago.forms import Form

class PostForm(Form):
    thread_name = forms.CharField(max_length=255)
    post = forms.CharField(widget=forms.Textarea)

    def __init__(self, data=None, file=None, request=None, mode=None, *args, **kwargs):
        self.mode = mode
        super(PostForm, self).__init__(data, file, request=request, *args, **kwargs)
    
    def finalize_form(self):
        self.layout = [
                       [
                        None,
                        [
                         ('thread_name', {'label': _("Thread Name")}),
                         ('post', {'label': _("Post Content")}),
                         ],
                        ],
                       ]
    
        if self.mode not in ['edit_thread', 'new_thread']:
            del self.fields['thread_name']
            del self.layout[0][1][0]
        

class QuickReplyForm(Form):
    post = forms.CharField(widget=forms.Textarea)