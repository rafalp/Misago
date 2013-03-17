from django.conf import settings
from django.core.urlresolvers import reverse as django_reverse
from django.db.models import Q
from django.shortcuts import redirect
from django.template import RequestContext
from django.utils.translation import ugettext as _
from misago.admin import site
from misago.apps.admin.widgets import *
from misago.models import Newsletter, User
from misago.apps.admin.newsletters.forms import NewsletterForm, SearchNewslettersForm

def reverse(route, target=None):
    if target:
        if route == 'admin_newsletters_send':
          return django_reverse(route, kwargs={'target': target.pk, 'token': target.token})
        return django_reverse(route, kwargs={'target': target.pk})
    return django_reverse(route)


"""
Views
"""
class List(ListWidget):
    admin = site.get_action('newsletters')
    id = 'list'
    columns = (
             ('newsletter', _("Newsletter")),
             )
    nothing_checked_message = _('You have to check at least one newsletter.')
    actions = (
             ('delete', _("Delete selected newsletters"), _("Are you sure you want to delete selected newsletters?")),
             )
    pagination = 20
    search_form = SearchNewslettersForm

    def sort_items(self, page_items, sorting_method):
        return page_items.order_by('-id')

    def set_filters(self, model, filters):
        if 'rank' in filters:
            model = model.filter(ranks__in=filters['rank']).distinct()
        if 'type' in filters:
            model = model.filter(ignore_subscriptions__in=filters['type'])
        if 'name' in filters:
            model = model.filter(name__icontains=filters['name'])
        if 'content' in filters:
            model = model.filter(Q(content_html__icontains=filters['content']) | Q(content_plain__icontains=filters['content']))
        return model

    def get_item_actions(self, item):
        return (
                self.action('envelope', _("Send Newsletter"), reverse('admin_newsletters_send', item)),
                self.action('pencil', _("Edit Newsletter"), reverse('admin_newsletters_edit', item)),
                self.action('remove', _("Delete Newsletter"), reverse('admin_newsletters_delete', item), post=True, prompt=_("Are you sure you want to delete this newsletter?")),
                )

    def action_delete(self, items, checked):
        Newsletter.objects.filter(id__in=checked).delete()
        return Message(_('Selected newsletters have been deleted successfully.'), 'success'), reverse('admin_newsletters')


class New(FormWidget):
    admin = site.get_action('newsletters')
    id = 'new'
    fallback = 'admin_newsletters'
    form = NewsletterForm
    submit_button = _("Save Newsletter")
    tabbed = True

    def get_new_url(self, model):
        return reverse('admin_newsletters_new')

    def get_edit_url(self, model):
        return reverse('admin_newsletters_edit', model)

    def submit_form(self, form, target):
        new_newsletter = Newsletter(
                      name=form.cleaned_data['name'],
                      step_size=form.cleaned_data['step_size'],
                      content_html=form.cleaned_data['content_html'],
                      content_plain=form.cleaned_data['content_plain'],
                      ignore_subscriptions=form.cleaned_data['ignore_subscriptions'],
                     )
        new_newsletter.generate_token()
        new_newsletter.save(force_insert=True)

        for rank in form.cleaned_data['ranks']:
            new_newsletter.ranks.add(rank)
        new_newsletter.save(force_update=True)

        return new_newsletter, Message(_('New Newsletter has been created.'), 'success')


class Edit(FormWidget):
    admin = site.get_action('newsletters')
    id = 'edit'
    name = _("Edit Newsletter")
    fallback = 'admin_newsletters'
    form = NewsletterForm
    target_name = 'name'
    notfound_message = _('Requested Newsletter could not be found.')
    submit_fallback = True
    tabbed = True

    def get_url(self, model):
        return reverse('admin_newsletters_edit', model)

    def get_edit_url(self, model):
        return self.get_url(model)

    def get_initial_data(self, model):
        return {
                'name': model.name,
                'step_size': model.step_size,
                'ignore_subscriptions': model.ignore_subscriptions,
                'content_html': model.content_html,
                'content_plain': model.content_plain,
                'ranks': model.ranks.all(),
                }

    def submit_form(self, form, target):
        target.name = form.cleaned_data['name']
        target.step_size = form.cleaned_data['step_size']
        target.ignore_subscriptions = form.cleaned_data['ignore_subscriptions']
        target.content_html = form.cleaned_data['content_html']
        target.content_plain = form.cleaned_data['content_plain']
        target.generate_token()

        target.ranks.clear()
        for rank in form.cleaned_data['ranks']:
            target.ranks.add(rank)

        target.save(force_update=True)
        return target, Message(_('Changes in newsletter "%(name)s" have been saved.') % {'name': self.original_name}, 'success')


class Delete(ButtonWidget):
    admin = site.get_action('newsletters')
    id = 'delete'
    fallback = 'admin_newsletters'
    notfound_message = _('Requested newsletter could not be found.')

    def action(self, target):
        target.delete()
        return Message(_('Newsletter "%(name)s"" has been deleted.') % {'name': target.name}, 'success'), False


def send(request, target, token):
    try:
        newsletter = Newsletter.objects.get(pk=target, token=token)

        # Build recipients queryset
        recipients = User.objects
        if newsletter.ranks.all():
            recipients = recipients.filter(rank__in=[x.pk for x in newsletter.ranks.all()])
        if not newsletter.ignore_subscriptions:
            recipients = recipients.filter(receive_newsletters=1)

        recipients_total = recipients.count()
        if recipients_total < 1:
            request.messages.set_flash(Message(_('No recipients for newsletter "%(newsletter)s" could be found.') % {'newsletter': newsletter.name}), 'error', 'newsletters')
            return redirect(reverse('admin_newsletters'))

        for user in recipients.all()[newsletter.progress:(newsletter.progress + newsletter.step_size)]:
            tokens = {
              '{{ board_name }}': request.settings.board_name,
              '{{ username }}': user.username,
              '{{ user_url }}': django_reverse('user', kwargs={'username': user.username_slug, 'user': user.pk}),
              '{{ board_url }}': settings.BOARD_ADDRESS,
            }
            subject = newsletter.parse_name(tokens)
            user.email_user(request, 'users/newsletter', subject, {
                                                                'newsletter': newsletter,
                                                                'subject': subject,
                                                                'content_html': newsletter.parse_html(tokens),
                                                                'content_plain': newsletter.parse_plain(tokens),
                                                                })
            newsletter.progress += 1
        newsletter.generate_token()
        newsletter.save(force_update=True)

        if newsletter.progress >= recipients_total:
            newsletter.progress = 0
            newsletter.save(force_update=True)
            request.messages.set_flash(Message(_('Newsletter "%(newsletter)s" has been sent.') % {'newsletter': newsletter.name}), 'success', 'newsletters')
            return redirect(reverse('admin_newsletters'))

        # Render Progress
        response = request.theme.render_to_response('processing.html', {
                'task_name': _('Sending Newsletter'),
                'target_name': newsletter.name,
                'message': _('Sent to %(progress)s from %(total)s users') % {'progress': newsletter.progress, 'total': recipients_total},
                'progress': newsletter.progress * 100 / recipients_total,
                'cancel_url': reverse('admin_newsletters'),
            }, context_instance=RequestContext(request));
        response['refresh'] = '2;url=%s' % reverse('admin_newsletters_send', newsletter)
        return response
    except Newsletter.DoesNotExist:
        request.messages.set_flash(Message(_('Requested Newsletter could not be found.')), 'error', 'newsletters')
        return redirect(reverse('admin_newsletters'))
