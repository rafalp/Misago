from django import forms
from django.core.urlresolvers import reverse
from django.db.models import F
from django.shortcuts import redirect
from django.template import RequestContext
from django.utils.translation import ugettext as _
from misago.authn.decorators import block_guest
from misago.forms import Form, FormLayout, FormFields
from misago.messages import Message
from misago.watcher.models import ThreadWatch
from misago.utils import make_pagination

@block_guest
def watched_threads(request, page=0, new=False):
    # Find mode and fetch threads
    queryset = ThreadWatch.objects.filter(user=request.user).filter(forum_id__in=request.acl.threads.get_readable_forums(request.acl)).select_related('thread').filter(thread__moderated=False).filter(thread__deleted=False)
    if new:
        queryset = queryset.filter(last_read__lt=F('thread__last'))
    count = queryset.count()
    pagination = make_pagination(page, count, request.settings.threads_per_page)
    queryset = queryset.order_by('-thread__last')
    if request.settings.threads_per_page < count:
        queryset = queryset[pagination['start']:pagination['stop']]
    queryset.prefetch_related('thread__forum', 'thread__last_poster')
    threads = []
    for thread in queryset:
        thread.thread.send_email = thread.email
        thread.thread.is_read = thread.thread.last <= thread.last_read             
        threads.append(thread.thread)
    
    # Build form and handle submit
    form = None
    message = request.messages.get_message('watcher')
    if threads:
        form_fields = {}
        form_fields['list_action'] = forms.ChoiceField(choices=(
                                                                ('mails', _("Send me e-mails")),
                                                                ('nomails', _("Don't send me e-mails")),
                                                                ('delete', _("Remove from watched threads")),
                                                                ))
        list_choices = []
        for item in threads:
            list_choices.append((item.pk, None))
        form_fields['list_items'] = forms.MultipleChoiceField(choices=list_choices, widget=forms.CheckboxSelectMultiple)
        form = type('ThreadsWatchForm', (Form,), form_fields)
        if request.method == 'POST':
            form = form(request.POST, request=request)
            if form.is_valid():
                checked_items = []
                for thread in threads:
                    if str(thread.pk) in form.cleaned_data['list_items']:
                        checked_items.append(thread.pk)
                if checked_items:
                    queryset = ThreadWatch.objects.filter(user=request.user).filter(thread_id__in = checked_items)
                    if form.cleaned_data['list_action'] == 'mails':
                        queryset.update(email=True)
                        request.messages.set_flash(Message(_('Selected threads will now send e-mails with notifications when somebody replies to them.')), 'success', 'watcher')
                    if form.cleaned_data['list_action'] == 'nomails':
                        queryset.update(email=False)
                        request.messages.set_flash(Message(_('Selected threads will no longer send e-mails with notifications when somebody replies to them.')), 'success', 'watcher')
                    if form.cleaned_data['list_action'] == 'delete':
                        queryset.delete()
                        request.messages.set_flash(Message(_('Selected threads have been removed from watched threads list.')), 'success', 'watcher')
                    return redirect(reverse('watched_threads_new' if new else 'watched_threads')) 
                else:
                    message = Message(_("You have to select at least one thread."), 'error')                    
            else:
                if 'list_action' in form.errors:
                    message = Message(_("Action requested is incorrect."), 'error')
                else:
                    message = Message(form.non_field_errors()[0], 'error')
        else:
            form = form(request=request)
            
    # Display page
    return request.theme.render_to_response('watched.html',
                                            {
                                             'total_items': count,
                                             'pagination': pagination,
                                             'new': new,
                                             'list_form': FormFields(form).fields if form else None,
                                             'threads': threads,
                                             'message': message,
                                             },
                                            context_instance=RequestContext(request))