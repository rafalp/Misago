from django.utils.translation import ugettext_lazy as _
from django import forms
from mptt.forms import TreeNodeChoiceField
from misago.forms import Form
from misago.forums.models import Forum

class CategoryForm(Form):
    parent = False
    name = forms.CharField(max_length=255)
    description = forms.CharField(widget=forms.Textarea,required=False)
    template = forms.ChoiceField(choices=(
                                          ('rows', _('One forum per row')),
                                          ('fifty', _('Two forums per row')),
                                          ('thirty', _('Three forums per row')),
                                          ))
    
    layout = (
              (
               _("Category Options"),
               (
                ('parent', {'label': _("Category Parent")}),
                ('name', {'label': _("Category Name")}),
                ('description', {'label': _("Category Description")}),
                ('template', {'label': _("Category Layout")}),
                ),
              ),
             )
    
    def __init__(self, *args, **kwargs):
        self.base_fields['parent'] = TreeNodeChoiceField(queryset=Forum.tree.get(token='root').get_descendants(include_self=True),level_indicator=u'- - ')
        super(CategoryForm, self).__init__(*args, **kwargs)
    

class ForumForm(Form):
    parent = False
    name = forms.CharField(max_length=255)
    description = forms.CharField(widget=forms.Textarea,required=False)
    template = forms.ChoiceField(choices=(
                                          ('rows', _('One forum per row')),
                                          ('fifty', _('Two forums per row')),
                                          ('thirty', _('Three forums per row')),
                                          ))
    prune_start = forms.IntegerField(min_value=0,initial=0)
    prune_last = forms.IntegerField(min_value=0,initial=0)
    
    layout = (
              (
               _("Forum Options"),
               (
                ('parent', {'label': _("Forum Parent")}),
                ('name', {'label': _("Forum Name")}),
                ('description', {'label': _("Forum Description")}),
                ('template', {'label': _("Subforums Layout")}),
                ),
              ),
              (
               _("Prune Forum"),
               (
                ('prune_start', {'label': _("Delete threads with first post older than"), 'help_text': _('Enter number of days since topic start after which topic will be deleted or zero to don\'t delete topics.')}),
                ('prune_last', {'label': _("Delete threads with last post older than"), 'help_text': _('Enter number of days since since last reply in topic after which topic will be deleted or zero to don\'t delete topics.')}),
                ),
              ),
             )
    
    def __init__(self, *args, **kwargs):
        self.base_fields['parent'] = TreeNodeChoiceField(queryset=Forum.tree.get(token='root').get_descendants(),level_indicator=u'- - ')
        super(ForumForm, self).__init__(*args, **kwargs)
        

class RedirectForm(Form):
    parent = False
    name = forms.CharField(max_length=255)
    description = forms.CharField(widget=forms.Textarea,required=False)
    redirect = forms.URLField(max_length=255)
    
    layout = (
              (
               _("Redirect Options"),
               (
                ('parent', {'label': _("Redirect Parent")}),
                ('name', {'label': _("Redirect Name")}),
                ('redirect', {'label': _("Redirect URL")}),
                ('description', {'label': _("Redirect Description")}),
                ),
              ),
             )
    
    def __init__(self, *args, **kwargs):
        self.base_fields['parent'] = TreeNodeChoiceField(queryset=Forum.tree.get(token='root').get_descendants(),level_indicator=u'- - ')
        super(RedirectForm, self).__init__(*args, **kwargs)
    

class DeleteForm(Form):
    parent = False
   
    layout = (
              (
               _("Delete Options"),
               (
                ('parent', {'label': _("Move deleted Forum contents to")}),
                ),
              ),
             )
        
    def __init__(self, *args, **kwargs):
        self.base_fields['parent'] = TreeNodeChoiceField(queryset=Forum.tree.get(token='root').get_descendants(),required=False,empty_label=_("Remove with forum"),level_indicator=u'- - ')
        super(DeleteForm, self).__init__(*args, **kwargs)