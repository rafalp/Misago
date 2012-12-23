import copy
from django.core.urlresolvers import reverse as django_reverse
from django.db.models import Q
from django.utils.translation import ugettext as _
from mptt.forms import TreeNodeChoiceField
from misago.admin import site
from misago.admin.widgets import *
from misago.utils import slugify
from misago.forums.forms import CategoryForm, ForumForm, RedirectForm, DeleteForm
from misago.forums.models import Forum

def reverse(route, target=None):
    if target:
        return django_reverse(route, kwargs={'target': target.pk, 'slug': target.slug})
    return django_reverse(route)

"""
Views
"""
class List(ListWidget):
    admin = site.get_action('forums')
    id = 'list'
    columns=(
             ('forum', _("Forum")),
             )
    nothing_checked_message = _('You have to select at least one forum.')
    actions=(
             ('resync', _("Resynchronise forums")),
             ('prune', _("Prune forums"), _("Are you sure you want to delete all content from selected forums?")),
             )
    empty_message = _('No forums are currently defined.')
    
    def get_items(self):
        return self.admin.model.objects.get(token='root').get_descendants()
    
    def sort_items(self, page_items, sorting_method):
        return page_items.order_by('lft')
    
    def get_item_actions(self, item):
        if item.type == 'category':
            return (
                    self.action('chevron-up', _("Move Category Up"), reverse('admin_forums_up', item), post=True),
                    self.action('chevron-down', _("Move Category Down"), reverse('admin_forums_down', item), post=True),
                    self.action('pencil', _("Edit Category"), reverse('admin_forums_edit', item)),
                    self.action('remove', _("Delete Category"), reverse('admin_forums_delete', item)),
                    )
            
        if item.type == 'forum':
            return (
                    self.action('chevron-up', _("Move Forum Up"), reverse('admin_forums_up', item), post=True),
                    self.action('chevron-down', _("Move Forum Down"), reverse('admin_forums_down', item), post=True),
                    self.action('pencil', _("Edit Forum"), reverse('admin_forums_edit', item)),
                    self.action('remove', _("Delete Forum"), reverse('admin_forums_delete', item)),
                    )
            
        return (
                self.action('chevron-up', _("Move Redirect Up"), reverse('admin_forums_up', item), post=True),
                self.action('chevron-down', _("Move Redirect Down"), reverse('admin_forums_down', item), post=True),
                self.action('pencil', _("Edit Redirect"), reverse('admin_forums_edit', item)),
                self.action('remove', _("Delete Redirect"), reverse('admin_forums_delete', item)),
                )

    def action_resync(self, items, checked):
        return Message(_('Selected forums have been resynchronised successfully.'), 'success'), reverse('admin_forums')

    def action_prune(self, items, checked):
        return Message(_('Selected forums have been pruned successfully.'), 'success'), reverse('admin_forums')


class NewCategory(FormWidget):
    admin = site.get_action('forums')
    id = 'new_category'
    fallback = 'admin_forums' 
    form = CategoryForm
    submit_button = _("Save Category")
        
    def get_new_url(self, model):
        return reverse('admin_forums_new_category')
    
    def get_edit_url(self, model):
        return reverse('admin_forums_edit', model)
    
    def submit_form(self, form, target):
        new_forum = Forum(
                     name=form.cleaned_data['name'],
                     template=form.cleaned_data['template'],
                     slug=slugify(form.cleaned_data['name']),
                     type='category',
                     style=form.cleaned_data['style'],
                     closed=form.cleaned_data['closed'],
                     )
        new_forum.set_description(form.cleaned_data['description'])
        new_forum.insert_at(form.cleaned_data['parent'], position='last-child', save=True)
        
        if form.cleaned_data['perms']:
            new_forum.copy_permissions(form.cleaned_data['perms'])
            self.request.monitor['acl_version'] = int(self.request.monitor['acl_version']) + 1
            
        return new_forum, Message(_('New Category has been created.'), 'success')


class NewForum(FormWidget):
    admin = site.get_action('forums')
    id = 'new_forum'
    fallback = 'admin_forums' 
    form = ForumForm
    submit_button = _("Save Forum")
        
    def get_new_url(self, model):
        return reverse('admin_forums_new_forum')
    
    def get_edit_url(self, model):
        return reverse('admin_forums_edit', model)
    
    def submit_form(self, form, target):
        new_forum = Forum(
                     name=form.cleaned_data['name'],
                     slug=slugify(form.cleaned_data['name']),
                     type='forum',
                     template=form.cleaned_data['template'],
                     style=form.cleaned_data['style'],
                     closed=form.cleaned_data['closed'],
                     prune_start=form.cleaned_data['prune_start'],
                     prune_last=form.cleaned_data['prune_last'],
                     )
        new_forum.set_description(form.cleaned_data['description'])
        new_forum.insert_at(form.cleaned_data['parent'], position='last-child', save=True)
        
        if form.cleaned_data['perms']:
            new_forum.copy_permissions(form.cleaned_data['perms'])
            self.request.monitor['acl_version'] = int(self.request.monitor['acl_version']) + 1
            
        return new_forum, Message(_('New Forum has been created.'), 'success')

    def __call__(self, request):
        if self.admin.model.objects.get(token='root').get_descendants().count() == 0:
            request.messages.set_flash(Message(_("You have to create at least one category before you will be able to create forums.")), 'error', self.admin.id)
            return redirect(self.get_fallback_url())
        return super(NewForum, self).__call__(request)


class NewRedirect(FormWidget):
    admin = site.get_action('forums')
    id = 'new_redirect'
    fallback = 'admin_forums' 
    form = RedirectForm
    submit_button = _("Save Forum")
        
    def get_new_url(self, model):
        return reverse('admin_forums_new_redirect')
    
    def get_edit_url(self, model):
        return reverse('admin_forums_edit', model)
    
    def submit_form(self, form, target):
        new_forum = Forum(
                     name=form.cleaned_data['name'],
                     slug=slugify(form.cleaned_data['name']),
                     redirect=form.cleaned_data['redirect'],
                     style=form.cleaned_data['style'],
                     type='redirect',
                     )
        new_forum.set_description(form.cleaned_data['description'])
        new_forum.insert_at(form.cleaned_data['parent'], position='last-child', save=True)
        
        if form.cleaned_data['perms']:
            new_forum.copy_permissions(form.cleaned_data['perms'])
            self.request.monitor['acl_version'] = int(self.request.monitor['acl_version']) + 1
            
        return new_forum, Message(_('New Redirect has been created.'), 'success')
    
    def __call__(self, request):
        if self.admin.model.objects.get(token='root').get_descendants().count() == 0:
            request.messages.set_flash(Message(_("You have to create at least one category before you will be able to create redirects.")), 'error', self.admin.id)
            return redirect(self.get_fallback_url())
        return super(NewRedirect, self).__call__(request)


class Up(ButtonWidget):
    admin = site.get_action('forums')
    id = 'up'
    fallback = 'admin_forums'
    notfound_message = _('Requested Forum could not be found.')
    
    def action(self, target):
        previous_sibling = target.get_previous_sibling()
        if previous_sibling:
            target.move_to(previous_sibling, 'left')
            return Message(_('Forum "%(name)s" has been moved up.') % {'name': target.name}, 'success'), False
        return Message(_('Forum "%(name)s" is first child of its parent node and cannot be moved up.') % {'name': target.name}, 'info'), False


class Down(ButtonWidget):
    admin = site.get_action('forums')
    id = 'down'
    fallback = 'admin_forums'
    notfound_message = _('Requested Forum could not be found.')
    
    def action(self, target):
        next_sibling = target.get_next_sibling()
        if next_sibling:
            target.move_to(next_sibling, 'right')
            return Message(_('Forum "%(name)s" has been moved down.') % {'name': target.name}, 'success'), False
        return Message(_('Forum "%(name)s" is last child of its parent node and cannot be moved down.') % {'name': target.name}, 'info'), False
  
   
class Edit(FormWidget):
    admin = site.get_action('forums')
    id = 'edit'
    name = _("Edit Forum")
    fallback = 'admin_forums'
    form = ForumForm
    target_name = 'name'
    notfound_message = _('Requested Forum could not be found.')
    submit_fallback = True
    
    def get_url(self, model):
        return reverse('admin_forums_edit', model)
    
    def get_edit_url(self, model):
        return self.get_url(model)
    
    def get_form(self, target):
        if target.type == 'category':
            self.name = _("Edit Category")
            self.form = CategoryForm
        if target.type == 'redirect':
            self.name = _("Edit Redirect")
            self.form = RedirectForm
        
        # Remove invalid targets from parent select
        self.form = copy.deepcopy(self.form)
        valid_targets = Forum.tree.get(token='root').get_descendants(include_self=target.type == 'category').exclude(Q(lft__gte=target.lft) & Q(rght__lte=target.rght))
        self.form.base_fields['parent'] = TreeNodeChoiceField(queryset=valid_targets,level_indicator=u'- - ')
        
        return self.form
    
    def get_initial_data(self, model):
        initial = {
                   'parent': model.parent,
                   'name': model.name,
                   'description': model.description,
                   }
            
        if model.type == 'redirect':
            initial['redirect'] = model.redirect
        else:
            initial['template'] = model.template
            initial['style'] = model.style
            initial['closed'] = model.closed
            
        if model.type == 'forum':
            initial['prune_start'] = model.prune_start
            initial['prune_last'] = model.prune_last
        
        return initial
    
    def submit_form(self, form, target):
        target.name = form.cleaned_data['name']
        target.set_description(form.cleaned_data['description'])
        if target.type == 'redirect':
            target.redirect = form.cleaned_data['redirect']
        else:
            target.template = form.cleaned_data['template']
            target.style = form.cleaned_data['style']
            target.closed = form.cleaned_data['closed']
            
        if target.type == 'forum':
            target.prune_start = form.cleaned_data['prune_start']
            target.prune_last = form.cleaned_data['prune_last']
            
        if form.cleaned_data['parent'].pk != target.parent.pk:
            target.move_to(form.cleaned_data['parent'], 'last-child')
            self.request.monitor['acl_version'] = int(self.request.monitor['acl_version']) + 1
            
        target.save(force_update=True)
            
        if form.cleaned_data['perms']:
            target.copy_permissions(form.cleaned_data['perms'])
        
        if form.cleaned_data['parent'].pk != target.parent.pk or form.cleaned_data['perms']:
            self.request.monitor['acl_version'] = int(self.request.monitor['acl_version']) + 1
        
        return target, Message(_('Changes in forum "%(name)s" have been saved.') % {'name': self.original_name}, 'success')


class Delete(FormWidget):
    admin = site.get_action('forums')
    id = 'delete'
    name = _("Delete Forum")
    fallback = 'admin_forums'
    template = 'delete'
    form = DeleteForm
    target_name = 'name'
    notfound_message = _('Requested Forum could not be found.')
    submit_fallback = True
    
    def get_url(self, model):
        return reverse('admin_forums_delete', model)
   
    def get_form(self, target):
        if target.type == 'category':
            self.name= _("Delete Category")
        if target.type == 'redirect':
            self.name= _("Delete Redirect")
        
        # Remove invalid targets from parent select
        self.form = copy.deepcopy(self.form)
        valid_targets = Forum.tree.get(token='root').get_descendants(include_self=target.type == 'category').exclude(Q(lft__gte=target.lft) & Q(rght__lte=target.rght))
        self.form.base_fields['parent'] = TreeNodeChoiceField(queryset=valid_targets,required=False,empty_label=_("Remove with forum"),level_indicator=u'- - ')
        
        return self.form
        
    def submit_form(self, form, target):
        new_parent = form.cleaned_data['parent']
        if new_parent:
            target.move_content(new_parent)
            for child in target.get_descendants():
                child.move_to(new_parent, 'last-child')
                child.save(force_update=True)
        else:
            for child in target.get_descendants():
                child.delete()
        target.delete()
        return target, Message(_('Forum "%(name)s" has been deleted.') % {'name': self.original_name}, 'success')