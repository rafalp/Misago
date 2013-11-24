from django.utils.translation import ugettext_lazy as _
from django import forms
from mptt.forms import TreeNodeChoiceField
from misago.forms import Form, YesNoSwitch
from misago.models import Forum
from misago.validators import validate_sluggable

class CleanAttrsMixin(object):
    def clean_attrs(self):
        clean = []
        data = self.cleaned_data['attrs'].strip().split()
        for i in data:
            i = i.strip()
            if not i in clean:
                clean.append(i)
        return ' '.join(clean)


class NewNodeForm(Form, CleanAttrsMixin):
    parent = False
    perms = False
    role = forms.ChoiceField(choices=(
                                      ('category', _("Category")),
                                      ('forum', _("Forum")),
                                      ('redirect', _("Redirection")),
                                      ))
    name = forms.CharField(max_length=255, validators=[validate_sluggable(
                                                                          _("Category name must contain alphanumeric characters."),
                                                                          _("Category name is too long.")
                                                                          )])
    redirect = forms.URLField(max_length=255, required=False)
    description = forms.CharField(widget=forms.Textarea, required=False)
    closed = forms.BooleanField(widget=YesNoSwitch, required=False)
    attrs = forms.CharField(max_length=255, required=False)
    show_details = forms.BooleanField(widget=YesNoSwitch, required=False, initial=True)
    style = forms.CharField(max_length=255, required=False)

    layout = (
              (
               _("Basic Options"),
               (
                ('parent', {'label': _("Node Parent")}),
                ('perms', {'label': _("Copy Permissions from")}),
                ('role', {'label': _("Node Type"), 'help_text': _("Each Node has specific role in forums tree. This role cannot be changed after node is created.")}),
                ('name', {'label': _("Node Name")}),
                ('description', {'label': _("Node Description")}),
                ('redirect', {'label': _("Redirect URL"), 'help_text': _("Redirection nodes require you to specify URL they will redirect users to upon click.")}),
                ('closed', {'label': _("Closed Node")}),
                ),
              ),
              (
               _("Display Options"),
               (
                ('attrs', {'label': _("Node Attributes"), 'help_text': _('Custom templates can check nodes for predefined attributes that will change way they are rendered.')}),
                ('show_details', {'label': _("Show Subforums Details"), 'help_text': _('Allows you to prevent this node subforums from displaying statistics, last post data, etc. ect. on forums lists.')}),
                ('style', {'label': _("Node Style"), 'help_text': _('You can add custom CSS classess to this node, to change way it looks on board index.')}),
                ),
              ),
             )

    def finalize_form(self):
        self.fields['parent'] = TreeNodeChoiceField(queryset=Forum.objects.get(special='root').get_descendants(include_self=True), level_indicator=u'- - ')
        self.fields['perms'] = TreeNodeChoiceField(queryset=Forum.objects.get(special='root').get_descendants(), level_indicator=u'- - ', required=False, empty_label=_("Don't copy permissions"))

    def clean(self):
        cleaned_data = super(NewNodeForm, self).clean()
        node_role = cleaned_data['role']

        if node_role != 'category' and cleaned_data['parent'].special == 'root':
            raise forms.ValidationError(_("Only categories can use Root Category as their parent."))
        if node_role == 'redirect' and not cleaned_data['redirect']:
            raise forms.ValidationError(_("You have to define redirection URL"))

        return cleaned_data



class CategoryForm(Form, CleanAttrsMixin):
    parent = False
    perms = False
    name = forms.CharField(max_length=255, validators=[validate_sluggable(
                                                                          _("Category name must contain alphanumeric characters."),
                                                                          _("Category name is too long.")
                                                                          )])
    description = forms.CharField(widget=forms.Textarea, required=False)
    closed = forms.BooleanField(widget=YesNoSwitch, required=False)
    style = forms.CharField(max_length=255, required=False)
    attrs = forms.CharField(max_length=255, required=False)
    show_details = forms.BooleanField(widget=YesNoSwitch, required=False, initial=True)

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
                ('attrs', {'label': _("Category Attributes"), 'help_text': _('Custom templates can check categories for predefined attributes that will change way they are rendered.')}),
                ('show_details', {'label': _("Show Subforums Details"), 'help_text': _('Allows you to prevent this category subforums from displaying statistics, last post data, etc. ect. on forums lists.')}),
                ('style', {'label': _("Category Style"), 'help_text': _('You can add custom CSS classess to this category, to change way it looks on board index.')}),
                ),
              ),
             )

    def finalize_form(self):
        self.fields['perms'] = TreeNodeChoiceField(queryset=Forum.objects.get(special='root').get_descendants(), level_indicator=u'- - ', required=False, empty_label=_("Don't copy permissions"))


class ForumForm(Form, CleanAttrsMixin):
    parent = False
    perms = False
    pruned_archive = False
    name = forms.CharField(max_length=255, validators=[validate_sluggable(
                                                                          _("Forum name must contain alphanumeric characters."),
                                                                          _("Forum name is too long.")
                                                                          )])
    description = forms.CharField(widget=forms.Textarea, required=False)
    closed = forms.BooleanField(widget=YesNoSwitch, required=False)
    style = forms.CharField(max_length=255, required=False)
    prune_start = forms.IntegerField(min_value=0, initial=0)
    prune_last = forms.IntegerField(min_value=0, initial=0)
    attrs = forms.CharField(max_length=255, required=False)
    show_details = forms.BooleanField(widget=YesNoSwitch, required=False, initial=True)

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
                ('pruned_archive', {'label': _("Archive pruned threads?"), 'help_text': _('If you want, you can archive pruned threads in other forum instead of deleting them.')})
                ),
               ),
              (
               _("Display Options"),
               (
                ('attrs', {'label': _("Forum Attributes"), 'help_text': _('Custom templates can check forums for predefined attributes that will change way subforums lists are rendered.')}),
                ('show_details', {'label': _("Show Subforums Details"), 'help_text': _("Allows you to prevent this forum's subforums from displaying statistics, last post data, etc. ect. on subforums list.")}),
                ('style', {'label': _("Forum Style"), 'help_text': _('You can add custom CSS classess to this forum to change way it looks on forums lists.')}),
                ),
               ),
              )

    def finalize_form(self):
        self.fields['perms'] = TreeNodeChoiceField(queryset=Forum.objects.get(special='root').get_descendants(), level_indicator=u'- - ', required=False, empty_label=_("Don't copy permissions"))
        self.fields['pruned_archive'] = TreeNodeChoiceField(queryset=Forum.objects.get(special='root').get_descendants(), level_indicator=u'- - ', required=False, empty_label=_("Don't archive pruned threads"))

    def clean_pruned_archive(self):
        data = self.cleaned_data['pruned_archive']
        if data and data.pk == self.target_forum.pk:
            raise forms.ValidationError(_("Forum cannot be its own archive."))
        return data


class RedirectForm(Form, CleanAttrsMixin):
    parent = False
    perms = False
    name = forms.CharField(max_length=255, validators=[validate_sluggable(
                                                                          _("Redirect name must contain alphanumeric characters."),
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
                ('attrs', {'label': _("Forum Attributes"), 'help_text': _('Custom templates can check forums for predefined attributes that will change way subforums lists are rendered.')}),
                ('style', {'label': _("Redirect Style"), 'help_text': _('You can add custom CSS classess to this redirect to change way it looks on forums lists.')}),
                ),
               ),
              )

    def finalize_form(self):
        self.fields['perms'] = TreeNodeChoiceField(queryset=Forum.objects.get(special='root').get_descendants(), level_indicator=u'- - ', required=False, empty_label=_("Don't copy permissions"))


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
        self.fields['contents'] = TreeNodeChoiceField(queryset=Forum.objects.get(special='root').get_descendants(), required=False, empty_label=_("Remove with forum"), level_indicator=u'- - ')
        self.fields['subforums'] = TreeNodeChoiceField(queryset=Forum.objects.get(special='root').get_descendants(), required=False, empty_label=_("Remove with forum"), level_indicator=u'- - ')

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
