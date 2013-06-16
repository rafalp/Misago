import copy
from urlparse import urlparse
from django.core.urlresolvers import resolve, reverse as django_reverse
from django.db.models import Q
from django.http import Http404
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from mptt.forms import TreeNodeChoiceField
from misago.admin import site
from misago.apps.admin.widgets import *
from misago.models import Forum
from misago.utils.strings import slugify
from misago.apps.admin.forums.forms import NewNodeForm, CategoryForm, ForumForm, RedirectForm, DeleteForm

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
    columns = (
               ('forum', _("Forum")),
               )
    nothing_checked_message = _('You have to select at least one forum.')
    actions = (
               ('resync_fast', _("Resynchronize forums (fast)")),
               ('resync', _("Resynchronize forums")),
               )
    empty_message = _('No forums are currently defined.')

    def get_items(self):
        return self.admin.model.objects.get(special='root').get_descendants()

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

    def action_resync_fast(self, items, checked):
        for forum in items:
            if forum.pk in checked:
                forum.sync()
                forum.save(force_update=True)
        return Message(_('Selected forums have been resynchronized successfully.'), 'success'), reverse('admin_forums')

    def action_resync(self, items, checked):
        clean_checked = []
        for item in items:
            if item.pk in checked and item.type == 'forum':
                clean_checked.append(item.pk)
        if not clean_checked:
            return Message(_('Only forums can be resynchronized.'), 'error'), reverse('admin_forums')
        self.request.session['sync_forums'] = clean_checked
        return Message('Meh', 'success'), django_reverse('admin_forums_resync')


def resync_forums(request, forum=0, progress=0):
    progress = int(progress)
    forums = request.session.get('sync_forums')
    if not forums:
        request.messages.set_flash(Message(_('No forums to resynchronize.')), 'info', 'forums')
        return redirect(reverse('admin_forums'))
    try:
        if not forum:
            forum = request.session['sync_forums'].pop()
        forum = Forum.objects.get(id=forum)
    except Forum.DoesNotExist:
        del request.session['sync_forums']
        request.messages.set_flash(Message(_('Forum for resynchronization does not exist.')), 'error', 'forums')
        return redirect(reverse('admin_forums'))

    # Sync 50 threads
    threads_total = forum.thread_set.count()
    for thread in forum.thread_set.all()[progress:(progress+1)]:
        thread.sync()
        thread.save(force_update=True)
        progress += 1

    if not threads_total:
        return redirect(django_reverse('admin_forums_resync'))

    # Render Progress
    response = request.theme.render_to_response('processing.html', {
            'task_name': _('Resynchronizing Forums'),
            'target_name': forum.name,
            'message': _('Resynchronized %(progress)s from %(total)s threads') % {'progress': progress, 'total': threads_total},
            'progress': progress * 100 / threads_total,
            'cancel_url': reverse('admin_forums'),
        }, context_instance=RequestContext(request));

    # Redirect where to?
    if progress >= threads_total:
        forum.sync()
        forum.save(force_update=True)
        response['refresh'] = '2;url=%s' % django_reverse('admin_forums_resync')
    else:
        response['refresh'] = '2;url=%s' % django_reverse('admin_forums_resync', kwargs={'forum': forum.pk, 'progress': progress})
    return response


class NewNode(FormWidget):
    admin = site.get_action('forums')
    id = 'new'
    fallback = 'admin_forums'
    form = NewNodeForm
    submit_button = _("Save Node")

    def get_new_url(self, model):
        return reverse('admin_forums_new')

    def get_edit_url(self, model):
        return reverse('admin_forums_edit', model)

    def get_initial_data(self, model):
        print 'CALL!'
        if not self.request.session.get('forums_admin_preffs'):
            print 'NO PATTERN!'
            return {}

        ref = self.request.META.get('HTTP_REFERER')
        if ref:
            parsed = urlparse(self.request.META.get('HTTP_REFERER'));
            try:
                link = resolve(parsed.path)
                if not link.url_name == 'admin_forums_new':
                    return {}
            except Http404:
                return {}
        try:
            init = self.request.session.get('forums_admin_preffs')
            del self.request.session['forums_admin_preffs']
            return {
                'parent': Forum.objects.get(id=init['parent']),
                'perms': Forum.objects.get(id=init['perms']) if init['perms'] else None,
                'role': init['role'],
            }
        except (KeyError, Forum.DoesNotExist):
            return {}

    def submit_form(self, form, target):
        new_forum = Forum(
                          name=form.cleaned_data['name'],
                          slug=slugify(form.cleaned_data['name']),
                          type=form.cleaned_data['role'],
                          attrs=form.cleaned_data['attrs'],
                          style=form.cleaned_data['style'],
                          )
        new_forum.set_description(form.cleaned_data['description'])

        if form.cleaned_data['role'] == 'redirect':
            new_forum.redirect = form.cleaned_data['redirect']
        else:
            new_forum.closed = form.cleaned_data['closed']
            new_forum.show_details = form.cleaned_data['show_details']

        new_forum.insert_at(form.cleaned_data['parent'], position='last-child', save=True)
        Forum.objects.populate_tree(True)

        if form.cleaned_data['perms']:
            new_forum.copy_permissions(form.cleaned_data['perms'])
            self.request.monitor.increase('acl_version')

        self.request.session['forums_admin_preffs'] = {
            'parent': form.cleaned_data['parent'].pk,
            'perms': form.cleaned_data['perms'].pk if form.cleaned_data['perms'] else None,
            'role': form.cleaned_data['role'],
        }

        if form.cleaned_data['role'] == 'category':
            return new_forum, Message(_('New Category has been created.'), 'success')
        if form.cleaned_data['role'] == 'forum':
            return new_forum, Message(_('New Forum has been created.'), 'success')
        if form.cleaned_data['role'] == 'redirect':
            return new_forum, Message(_('New Redirect has been created.'), 'success')


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
        return self.form

    def get_form_instance(self, form, target, initial, post=False):
        form_inst = super(Edit, self).get_form_instance(form, target, initial, post)
        valid_targets = Forum.objects.get(special='root').get_descendants(include_self=target.type == 'category').exclude(Q(lft__gte=target.lft) & Q(rght__lte=target.rght))
        form_inst.fields['parent'] = TreeNodeChoiceField(queryset=valid_targets, level_indicator=u'- - ')
        form_inst.target_forum = target
        return form_inst

    def get_initial_data(self, model):
        initial = {
                   'parent': model.parent,
                   'name': model.name,
                   'description': model.description,
                   }

        if model.type == 'redirect':
            initial['redirect'] = model.redirect
        else:
            initial['attrs'] = model.attrs
            initial['show_details'] = model.show_details
            initial['style'] = model.style
            initial['closed'] = model.closed

        if model.type == 'forum':
            initial['prune_start'] = model.prune_start
            initial['prune_last'] = model.prune_last
            initial['pruned_archive'] = model.pruned_archive

        return initial

    def submit_form(self, form, target):
        target.name = form.cleaned_data['name']
        target.slug = slugify(form.cleaned_data['name'])
        target.set_description(form.cleaned_data['description'])
        if target.type == 'redirect':
            target.redirect = form.cleaned_data['redirect']
        else:
            target.attrs = form.cleaned_data['attrs']
            target.show_details = form.cleaned_data['show_details']
            target.style = form.cleaned_data['style']
            target.closed = form.cleaned_data['closed']

        if target.type == 'forum':
            target.prune_start = form.cleaned_data['prune_start']
            target.prune_last = form.cleaned_data['prune_last']
            target.pruned_archive = form.cleaned_data['pruned_archive']

        if form.cleaned_data['parent'].pk != target.parent.pk:
            target.move_to(form.cleaned_data['parent'], 'last-child')
            self.request.monitor.increase('acl_version')

        target.save(force_update=True)
        Forum.objects.populate_tree(True)

        if form.cleaned_data['perms']:
            target.copy_permissions(form.cleaned_data['perms'])

        if form.cleaned_data['parent'].pk != target.parent.pk or form.cleaned_data['perms']:
            self.request.monitor.increase('acl_version')

        if self.original_name != target.name:
            target.sync_name()

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
            self.name = _("Delete Category")
        if target.type == 'redirect':
            self.name = _("Delete Redirect")
        return self.form

    def get_form_instance(self, form, target, initial, post=False):
        if post:
            form_inst = form(self.request.POST, forum=target, request=self.request, initial=self.get_initial_data(target))
        else:
            form_inst = form(forum=target, request=self.request, initial=self.get_initial_data(target))
        if target.type != 'forum':
            del form_inst.fields['contents']
        valid_targets = Forum.objects.get(special='root').get_descendants().exclude(Q(lft__gte=target.lft) & Q(rght__lte=target.rght))
        form_inst.fields['subforums'] = TreeNodeChoiceField(queryset=valid_targets, required=False, empty_label=_("Remove with forum"), level_indicator=u'- - ')
        return form_inst

    def submit_form(self, form, target):
        if target.type == 'forum':
            new_forum = form.cleaned_data['contents']
            if new_forum:
                target.move_content(new_forum)
                new_forum.sync()
                new_forum.save(force_update=True)
        new_parent = form.cleaned_data['subforums']
        if new_parent:
            for child in target.get_descendants():
                if child.parent_id == target.pk:
                    child.move_to(new_parent, 'last-child')
                    child.save(force_update=True)
        else:
            for child in target.get_descendants().order_by('-lft'):
                Forum.objects.get(id=child.pk).delete()
        Forum.objects.get(id=target.pk).delete()
        Forum.objects.populate_tree(True)
        self.request.monitor.increase('acl_version')
        return target, Message(_('Forum "%(name)s" has been deleted.') % {'name': self.original_name}, 'success')
