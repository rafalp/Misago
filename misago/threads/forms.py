from django import forms
from django.utils.translation import ungettext, ugettext_lazy as _
from misago.forms import Form
from misago.utils import slugify

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
            
    def clean_thread_name(self):
        data = self.cleaned_data['thread_name']
        slug = slugify(data)
        if len(slug) < self.request.settings['thread_name_min']:
            raise forms.ValidationError(ungettext(
                                                  "Thread name must contain at least one alpha-numeric character.",
                                                  "Thread name must contain at least %(count)d alpha-numeric characters.",
                                                  self.request.settings['thread_name_min']
                                                  ) % {'count': self.request.settings['thread_name_min']})
        return data
            
    def clean_post(self):
        data = self.cleaned_data['post']
        if len(data) < self.request.settings['post_length_min']:
            raise forms.ValidationError(ungettext(
                                                  "Post content cannot be empty.",
                                                  "Post content cannot be shorter than %(count)d characters.",
                                                  self.request.settings['post_length_min']
                                                  ) % {'count': self.request.settings['post_length_min']})
        return data
        
        

class QuickReplyForm(Form):
    post = forms.CharField(widget=forms.Textarea)