from django.core.urlresolvers import reverse as django_reverse
from django import forms
from django.utils.translation import ungettext, ugettext as _
from misago.admin import site
from misago.apps.admin.widgets import *
from misago.forms import Form
from misago.models import PruningPolicy, User
from misago.shortcuts import render_to_response
from misago.apps.admin.pruneusers.forms import PolicyForm

def reverse(route, target=None):
    if target:
        return django_reverse(route, kwargs={'target': target.pk})
    return django_reverse(route)


"""
Views
"""
class List(ListWidget):
    admin = site.get_action('prune_users')
    id = 'list'
    columns = (
               ('name', _("Pruning Policy")),
               )
    nothing_checked_message = _('You have to check at least one policy.')
    actions = (
               ('delete', _("Delete selected policies"), _("Are you sure you want to delete selected policies?")),
               )

    def sort_items(self, page_items, sorting_method):
        return page_items.order_by('name')

    def get_item_actions(self, item):
        return (
                self.action('filter', _("Apply Policy"), reverse('admin_prune_users_apply', item)),
                self.action('pencil', _("Edit Policy"), reverse('admin_prune_users_edit', item)),
                self.action('remove', _("Delete Policy"), reverse('admin_prune_users_delete', item), post=True, prompt=_("Are you sure you want to delete this policy?")),
                )

    def action_delete(self, items, checked):
        if not self.request.user.is_god():
            return Message(_('Only system administrators can delete pruning policies.'), 'error'), reverse('admin_prune_users')

        PruningPolicy.objects.filter(id__in=checked).delete()
        return Message(_('Selected pruning policies have been deleted successfully.'), 'success'), reverse('admin_prune_users')


class New(FormWidget):
    admin = site.get_action('prune_users')
    id = 'new'
    fallback = 'admin_prune_users'
    form = PolicyForm
    submit_button = _("Save Policy")

    def get_new_url(self, model):
        return reverse('admin_prune_users_new')

    def get_edit_url(self, model):
        return reverse('admin_prune_users_edit', model)

    def submit_form(self, form, target):
        new_policy = PruningPolicy(
                      name=form.cleaned_data['name'],
                      email=form.cleaned_data['email'],
                      posts=form.cleaned_data['posts'],
                      registered=form.cleaned_data['registered'],
                      last_visit=form.cleaned_data['last_visit'],
                     )
        new_policy.clean()
        new_policy.save(force_insert=True)

        return new_policy, Message(_('New Pruning Policy has been created.'), 'success')

    def __call__(self, request, *args, **kwargs):
        if not request.user.is_god():
            request.messages.set_flash(Message(_('Only system administrators can set new pruning policies.')), 'error', self.admin.id)
            return redirect(reverse('admin_prune_users'))

        return super(New, self).__call__(request, *args, **kwargs)


class Edit(FormWidget):
    admin = site.get_action('prune_users')
    id = 'edit'
    name = _("Edit Pruning Policy")
    fallback = 'admin_prune_users'
    form = PolicyForm
    target_name = 'name'
    notfound_message = _('Requested pruning policy could not be found.')
    submit_fallback = True

    def get_url(self, model):
        return reverse('admin_prune_users_edit', model)

    def get_edit_url(self, model):
        return self.get_url(model)

    def get_initial_data(self, model):
        return {
                'name': model.name,
                'email': model.email,
                'posts': model.posts,
                'registered': model.registered,
                'last_visit': model.last_visit,
                }

    def submit_form(self, form, target):
        target.name = form.cleaned_data['name']
        target.email = form.cleaned_data['email']
        target.posts = form.cleaned_data['posts']
        target.registered = form.cleaned_data['registered']
        target.last_visit = form.cleaned_data['last_visit']
        target.clean()
        target.save(force_update=True)

        return target, Message(_('Changes in policy "%(name)s" have been saved.') % {'name': self.original_name}, 'success')

    def __call__(self, request, *args, **kwargs):
        if not request.user.is_god():
            request.messages.set_flash(Message(_('Only system administrators can edit pruning policies.')), 'error', self.admin.id)
            return redirect(reverse('admin_prune_users'))

        return super(Edit, self).__call__(request, *args, **kwargs)


class Delete(ButtonWidget):
    admin = site.get_action('prune_users')
    id = 'delete'
    fallback = 'admin_prune_users'
    notfound_message = _('Requested pruning policy could not be found.')

    def action(self, target):
        if not self.request.user.is_god():
            return Message(_('Only system administrators can delete pruning policies.'), 'error'), False

        target.delete()
        return Message(_('Pruning policy "%(name)s" has been deleted.') % {'name': target.name}, 'success'), False


class Apply(FormWidget):
    admin = site.get_action('prune_users')
    id = 'apply'
    name = _("Apply Pruning Policy")
    fallback = 'admin_prune_users'
    form = PolicyForm
    target_name = 'name'
    notfound_message = _('Requested pruning policy could not be found.')
    submit_fallback = True
    template = 'apply'

    def get_url(self, model):
        return reverse('admin_prune_users_apply', model)

    def __call__(self, request, target=None, slug=None):
        self.request = request

        # Fetch target
        model = None
        if target:
            model = self.get_and_validate_target(target)
            self.original_name = self.get_target_name(model)
            if not model:
                return redirect(self.get_fallback_url())
        original_model = model

        # Set filter
        users = model.get_model()
        total_users = users
        total_users = total_users.count()

        if not total_users:
            request.messages.set_flash(Message(_('Policy "%(name)s" does not apply to any users.') % {'name': model.name}), 'error', self.admin.id)
            return redirect(reverse('admin_prune_users'))

        message = None
        if request.method == 'POST':
            deleted = 0
            if request.csrf.request_secure(request):
                for user in users.iterator():
                    if user.is_protected():
                        request.messages.set_flash(Message(_('User "%(name)s" is protected and was not deleted.') % {'name': user.username}), 'info', self.admin.id)
                    else:
                        user.delete()
                        deleted += 1
                if deleted:
                    request.messages.set_flash(Message(ungettext(
                                                                 'One user has been deleted.',
                                                                 '%(deleted)d users have been deleted.',
                                                                 deleted
                                                                 ) % {'deleted': deleted}), 'success', self.admin.id)
                    User.objects.resync_monitor()
                else:
                    request.messages.set_flash(Message(_("No users have been deleted.")), 'info', self.admin.id)
                return redirect(reverse('admin_prune_users'))
            else:
                message = Message(_("Request authorization is invalid. Please resubmit your form."), 'error')

        return render_to_response(self.get_template(),
                                  {
                                  'admin': self.admin,
                                  'action': self,
                                  'request': request,
                                  'url': self.get_url(model),
                                  'fallback': self.get_fallback_url(),
                                  'messages': request.messages.get_messages(self.admin.id),
                                  'message': message,
                                  'tabbed': self.tabbed,
                                  'total_users': total_users,
                                  'target': self.get_target_name(original_model),
                                  'target_model': original_model,
                                  },
                                  context_instance=RequestContext(request));
