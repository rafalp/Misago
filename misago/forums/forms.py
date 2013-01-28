from django.utils.translation import ugettext_lazy as _
from django import forms
from mptt.forms import TreeNodeChoiceField
from misago.forms import Form, YesNoSwitch
from misago.forums.models import Forum
from misago.utils.validators import validate_sluggable

class CategoryForm(Form):
    parent = False
    perms = False
    name = forms.CharField(max_length=255, validators=[validate_sluggable(
                                                                          _("Category name must be sluggable."),
                                                                          _("Category name is too long.")
                                                                          )])
    description = forms.CharField(widget=forms.Textarea, required=False)
    closed = forms.BooleanField(widget=YesNoSwitch, required=False)
    style = forms.CharField(max_length=255, required=False)
    template = forms.ChoiceField(choices=(
                                          ('row', _('One forum per row')),
                                          ('half', _('Two forums per row')),
                                          ('quarter', _('Four forums per row')),
                                          ))
    show_details = forms.BooleanField(widget=YesNoSwitch, required=False)

    layout = (
              (
               _("Basic Options"),
               (
                ('parent', {'label': _("Category Parent")}),
                ('perms', {'label': _("Copy Permissions from")}),
                ('name', {'label': _("Category Name")}),
                ('description', {'label': _("Category Description")}),
                ('closed', {'label': _("Closed Category")}),
                ),
              ),
              (
               _("Display Options"),
               (
                ('template', {'label': _("Category Layout"), 'help_text': _('Controls how this category is displayed on forums lists.')}),
                ('show_details', {'label': _("Show Subforums Details"), 'help_text': _('Allows you to prevent this category subforums from displaying statistics, last post data, etc. ect. on forums lists.')}),
                ('style', {'label': _("Category Style"), 'help_text': _('You can add custom CSS classess to this category, to change way it looks on board index.')}),
                ),
              ),
             )

    def finalize_form(self):
        self.fields['parent'] = TreeNodeChoiceField(queryset=Forum.tree.get(token='root').get_descendants(include_self=True), level_indicator=u'- - ')
        self.fields['perms'] = TreeNodeChoiceField(queryset=Forum.tree.get(token='root').get_descendants(), level_indicator=u'- - ', required=False, empty_label=_("Don't copy permissions"))


class ForumForm(Form):
    parent = False
    perms = False
    name = forms.CharField(max_length=255, validators=[validate_sluggable(
                                                                          _("Forum name must be sluggable."),
                                                                          _("Forum name is too long.")
                                                                          )])
    description = forms.CharField(widget=forms.Textarea, required=False)
    closed = forms.BooleanField(widget=YesNoSwitch, required=False)
    style = forms.CharField(max_length=255, required=False)
    prune_start = forms.IntegerField(min_value=0, initial=0)
    prune_last = forms.IntegerField(min_value=0, initial=0)
    template = forms.ChoiceField(choices=(
                                          ('row', _('One forum per row')),
                                          ('half', _('Two forums per row')),
                                          ('quarter', _('Four forums per row')),
                                          ))
    show_details = forms.BooleanField(widget=YesNoSwitch, required=False)

    layout = (
              (
               _("Basic Options"),
               (
                ('parent', {'label': _("Forum Parent")}),
                ('perms', {'label': _("Copy Permissions from")}),
                ('name', {'label': _("Forum Name")}),
                ('description', {'label': _("Forum Description")}),
                ('closed', {'label': _("Closed Forum")}),
                ),
               ),
              (
               _("Prune Forum"),
               (
                ('prune_start', {'label': _("Delete threads with first post older than"), 'help_text': _('Enter number of days since thread start after which thread will be deleted or zero to don\'t delete threads.')}),
                ('prune_last', {'label': _("Delete threads with last post older than"), 'help_text': _('Enter number of days since since last reply in thread after which thread will be deleted or zero to don\'t delete threads.')}),
                ),
               ),
              (
               _("Display Options"),
               (
                ('template', {'label': _("Subforums Layout"), 'help_text': _('Controls how this forum displays subforums list.')}),
                ('show_details', {'label': _("Show Subforums Details"), 'help_text': _("Allows you to prevent this forum's subforums from displaying statistics, last post data, etc. ect. on subforums list.")}),
                ('style', {'label': _("Forum Style"), 'help_text': _('You can add custom CSS classess to this forum to change way it looks on forums lists.')}),
                ),
               ),
              )

    def finalize_form(self):
        self.fields['parent'] = TreeNodeChoiceField(queryset=Forum.tree.get(token='root').get_descendants(), level_indicator=u'- - ')
        self.fields['perms'] = TreeNodeChoiceField(queryset=Forum.tree.get(token='root').get_descendants(), level_indicator=u'- - ', required=False, empty_label=_("Don't copy permissions"))


class RedirectForm(Form):
    parent = False
    perms = False
    name = forms.CharField(max_length=255, validators=[validate_sluggable(
                                                                          _("Redirect name must be sluggable."),
                                                                          _("Redirect name is too long.")
                                                                          )])
    description = forms.CharField(widget=forms.Textarea, required=False)
    redirect = forms.URLField(max_length=255)
    style = forms.CharField(max_length=255, required=False)

    layout = (
              (
               _("Basic Options"),
               (
                ('parent', {'label': _("Redirect Parent")}),
                ('perms', {'label': _("Copy Permissions from")}),
                ('name', {'label': _("Redirect Name")}),
                ('redirect', {'label': _("Redirect URL")}),
                ('description', {'label': _("Redirect Description")}),
                ),
               ),
              (
               _("Display Options"),
               (
                ('style', {'label': _("Redirect Style"), 'help_text': _('You can add custom CSS classess to this redirect to change way it looks on forums lists.')}),
                ),
               ),
              )

    def finalize_form(self):
        self.fields['parent'] = TreeNodeChoiceField(queryset=Forum.tree.get(token='root').get_descendants(), level_indicator=u'- - ')
        self.fields['perms'] = TreeNodeChoiceField(queryset=Forum.tree.get(token='root').get_descendants(), level_indicator=u'- - ', required=False, empty_label=_("Don't copy permissions"))


class DeleteForm(Form):
    layout = (
              (
               _("Delete Options"),
               (
                ('contents', {'label': _("Move threads to")}),
                ('subforums', {'label': _("Move subforums to")}),
                ),
               ),
              )

    def __init__(self, *args, **kwargs):
        self.forum = kwargs.pop('forum')
        super(DeleteForm, self).__init__(*args, **kwargs)

    def finalize_form(self):
        self.fields['contents'] = TreeNodeChoiceField(queryset=Forum.tree.get(token='root').get_descendants(), required=False, empty_label=_("Remove with forum"), level_indicator=u'- - ')
        self.fields['subforums'] = TreeNodeChoiceField(queryset=Forum.tree.get(token='root').get_descendants(), required=False, empty_label=_("Remove with forum"), level_indicator=u'- - ')

    def clean_contents(self):
        data = self.cleaned_data['contents']
        if data:
            if data.type == 'category':
                raise forms.ValidationError(_("Categories cannot contain threads."))
            if data.type == 'redirect':
                raise forms.ValidationError(_("Redirects cannot contain threads."))
        return data

    def clean(self):
        cleaned_data = super(DeleteForm, self).clean()
        if self.forum.type == 'forum' and cleaned_data['contents'] and cleaned_data['contents'].lft > self.forum.lft and cleaned_data['contents'].rght < self.forum.rght and not cleaned_data['subforums']:
            raise forms.ValidationError(_("Destination you want to move this forum's threads to will be deleted with this forum."))
        return cleaned_data
