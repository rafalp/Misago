from django import forms
from django.utils.translation import ungettext, ugettext_lazy as _
from mptt.forms import TreeNodeChoiceField
from misago.forms import Form
from misago.forums.models import Forum
from misago.utils import slugify

class ThreadNameMixin(object):
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


class PostForm(Form, ThreadNameMixin):
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


class MoveThreadsForm(Form):
    error_source = 'new_forum'
    
    def __init__(self, data=None, request=None, forum=None, *args, **kwargs):
        self.forum = forum
        super(MoveThreadsForm, self).__init__(data, request=request, *args, **kwargs)
    
    def finalize_form(self):
        self.fields['new_forum'] = TreeNodeChoiceField(queryset=Forum.tree.get(token='root').get_descendants().filter(pk__in=self.request.acl.forums.acl['can_browse']),level_indicator=u'- - ')
        self.layout = [
                       [
                        _("Thread Options"),
                        [
                         ('new_forum', {'label': _("Move Thread to"), 'help_text': _("Select forum you want to move threads to.")}),
                         ],
                        ],
                       ]
            
    def clean_new_forum(self):
        new_forum = self.cleaned_data['new_forum']
        # Assert its forum and its not current forum
        if new_forum.type != 'forum':
            raise forms.ValidationError(_("This is not forum."))
        if new_forum.pk == self.forum.pk:
            raise forms.ValidationError(_("New forum is same as current one."))
        return new_forum


class MergeThreadsForm(Form, ThreadNameMixin):
    def __init__(self, data=None, request=None, threads=[], *args, **kwargs):
        self.threads = threads
        super(MergeThreadsForm, self).__init__(data, request=request, *args, **kwargs)
    
    def finalize_form(self):
        self.fields['thread_name'] = forms.CharField(max_length=255, initial=self.threads[0].name)
        self.layout = [
                       [
                        _("Thread Options"),
                        [
                         ('thread_name', {'label': _("Thread Name"), 'help_text': _("Name of new thread that will be created as result of merge.")}),
                         ],
                        ],
                       [
                        _("Merge Order"),
                        [
                         ],
                        ],
                       ]
        
        choices = []
        for i, thread in enumerate(self.threads):
            choices.append((str(i), i + 1))
        for i, thread in enumerate(self.threads):
            self.fields['thread_%s' % thread.pk] = forms.ChoiceField(choices=choices,initial=str(i))
            self.layout[1][1].append(('thread_%s' % thread.pk, {'label': thread.name}))
            
    def clean(self):        
        cleaned_data = super(MergeThreadsForm, self).clean()
        self.merge_order = {}
        lookback = []
        for thread in self.threads:
            order = int(cleaned_data['thread_%s' % thread.pk])
            if order in lookback:
                raise forms.ValidationError(_("One or more threads have same position in merge order."))
            lookback.append(order)
            self.merge_order[order] = thread
        return cleaned_data