import math
from datetime import datetime, timedelta
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.http import Http404
from django.shortcuts import redirect
from django.template import RequestContext
from django.utils import formats, timezone
from django.utils.translation import ugettext as _
from misago.admin import site
from misago.admin.widgets import *
from misago.forms import FormLayout
from misago.forums.models import Thread, Post
from misago.messages import Message, BasicMessage
from misago.overview.admin.forms import GenerateStatisticsForm, SearchSessionsForm
from misago.sessions.models import Session
from misago.users.models import User

def overview_home(request):
    return request.theme.render_to_response('overview/home.html', {
        'users': request.monitor['users'],
        'users_inactive': request.monitor['users_inactive'],
        'threads': request.monitor['threads'],
        'posts': request.monitor['posts'],
        'admins': Session.objects.filter(user__isnull=False).filter(admin=1).order_by('user__username_slug').select_related(depth=1),
        }, context_instance=RequestContext(request));


def overview_stats(request):
    """
    Allow admins to generate fancy statistic graphs for different models
    """
    statistics_providers = []
    models_map = {}
    for model in models.get_models():
        try:
            getattr(model.objects, 'filter_overview')
            statistics_providers.append((str(model.__name__).lower(), model.statistics_name))
            models_map[str(model.__name__).lower()] = model
        except AttributeError:
            pass

    if not statistics_providers:
        """
        Something went FUBAR - Misago ships with some stats providers out of box
        If those providers cant be found, this means Misago filesystem is corrupted
        """
        return request.theme.render_to_response('overview/stats/not_available.html',
                                                context_instance=RequestContext(request));
    
    message = None
    if request.method == 'POST':
        form = GenerateStatisticsForm(request.POST, provider_choices=statistics_providers, request=request)
        if form.is_valid():
            date_start = form.cleaned_data['date_start']
            date_end = form.cleaned_data['date_end']
            if date_start > date_end:
                # Reverse dates if start is after end
                date_temp = date_end
                date_end = date_start
                date_start = date_temp
            # Assert that dates are correct
            if date_end == date_start:
                message = BasicMessage(_('Start and end date are same'), type='error')
            elif check_dates(date_start, date_end, form.cleaned_data['stats_precision']):
                message = check_dates(date_start, date_end, form.cleaned_data['stats_precision'])
            else:
                request.messages.set_flash(BasicMessage(_('Statistical report has been created.')), 'success', 'admin_stats')
                return redirect(reverse('admin_overview_graph', kwargs={
                                                       'model': form.cleaned_data['provider_model'],
                                                       'date_start': date_start.strftime('%Y-%m-%d'),
                                                       'date_end': date_end.strftime('%Y-%m-%d'),
                                                       'precision': form.cleaned_data['stats_precision']
                                                        }))
        else:
            message = Message(request, form.non_field_errors()[0])
            message.type = 'error'
    else:
        form = GenerateStatisticsForm(provider_choices=statistics_providers, request=request)
    
    return request.theme.render_to_response('overview/stats/form.html', {
                                            'form': FormLayout(form),
                                            'message': message,
                                            }, context_instance=RequestContext(request));


def overview_graph(request, model, date_start, date_end, precision):
    """
    Generate fancy graph for model and stuff
    """
    if date_start == date_end:
        # Bad dates
        raise Http404()
    
    # Turn stuff into datetime's
    date_start = datetime.strptime(date_start, '%Y-%m-%d')
    date_end = datetime.strptime(date_end, '%Y-%m-%d')
    
    
    statistics_providers = []
    models_map = {}
    for model_obj in models.get_models():
        try:
            getattr(model_obj.objects, 'filter_overview')
            statistics_providers.append((str(model_obj.__name__).lower(), model_obj.statistics_name))
            models_map[str(model_obj.__name__).lower()] = model_obj
        except AttributeError:
            pass

    if not statistics_providers:
        # Like before, q.q on lack of models
        return request.theme.render_to_response('overview/stats/not_available.html',
                                                context_instance=RequestContext(request));
    
    if not model in models_map or check_dates(date_start, date_end, precision):
        # Bad model name or graph data!
        raise Http404()
    
    form = GenerateStatisticsForm(
                                  provider_choices=statistics_providers,
                                  request=request,
                                  initial={'provider_model': model, 'date_start': date_start, 'date_end': date_end, 'stats_precision': precision})
    return request.theme.render_to_response('overview/stats/graph.html', {
                                            'title': models_map[model].statistics_name,
                                            'graph': build_graph(models_map[model], date_start, date_end, precision),
                                            'form': FormLayout(form),
                                            'message': request.messages.get_message('admin_stats'),
                                            }, context_instance=RequestContext(request));


def check_dates(date_start, date_end, precision):
    date_diff = date_end - date_start
    date_diff = date_diff.seconds + date_diff.days * 86400
    
    if ((precision == 'day' and date_diff / 86400 > 60)
        or (precision == 'week' and date_diff / 604800 > 60)
        or (precision == 'month' and date_diff / 2592000 > 60)
        or (precision == 'year' and date_diff / 31536000 > 60)):
        return BasicMessage(_('Too many many items to display on graph.'), type='error')
    elif ((precision == 'day' and date_diff / 86400 < 1)
          or (precision == 'week' and date_diff / 604800 < 1)
          or (precision == 'month' and date_diff / 2592000 < 1)
          or (precision == 'year' and date_diff / 31536000 < 1)):
        return BasicMessage(_('Too few items to display on graph'), type='error')
    return None
        
def build_graph(model, date_start, date_end, precision):
    if precision == 'day':
        format = 'F j, Y'
        step = 86400
    if precision == 'week':
        format = 'W, Y'
        step = 604800
    if precision == 'month':
        format = 'F, Y'
        step = 2592000
    if precision == 'year':
        format = 'Y'
        step = 31536000
    
    date_end = timezone.make_aware(date_end, timezone.get_current_timezone())
    date_start = timezone.make_aware(date_start, timezone.get_current_timezone())
    
    date_diff = date_end - date_start
    date_diff = date_diff.seconds + date_diff.days * 86400
    steps = int(math.ceil(float(date_diff / step))) + 1
    timeline = [0 for i in range(0, steps)]
    for i in range(0, steps):
        step_date = date_end - timedelta(seconds=(i * step));
        timeline[steps - i - 1] = step_date    
    stat = {'total': 0, 'max': 0, 'stat': [0 for i in range(0, steps)], 'timeline': timeline, 'start': date_start, 'end': date_end, 'format': format}
        
    # Loop model items
    for item in model.objects.filter_overview(date_start, date_end).iterator():
        date_diff = date_end - item.get_date()
        date_diff = date_diff.seconds + date_diff.days * 86400
        date_diff = steps - int(math.floor(float(date_diff / step))) - 2
        stat['stat'][date_diff] += 1
        stat['total'] += 1
        
    # Find max
    for i in stat['stat']:
        if i > stat['max']:
            stat['max'] = i
    return stat


class OnlineList(ListWidget):
    admin = site.get_action('online')
    id = 'list'
    columns=(
             ('owner', _("Session Owner")),
             ('start', _("Session Start"), 25),
             ('last', _("Last Click"), 25),
             )
    default_sorting = 'start'
    sortables={
               'start': 0,
               'last': 0,
              }
    hide_actions = True
    pagination = 50
    search_form = SearchSessionsForm
    empty_message = _('Looks like nobody is currently online on forums.')
    
    def set_filters(self, model, filters):
        if 'username' in filters:
            model = model.filter(user__username__istartswith=filters['username'])
        if 'ip_address' in filters:
            model = model.filter(ip__startswith=filters['ip_address'])
        if 'useragent' in filters:
            model = model.filter(agent__icontains=filters['useragent'])
        if filters['type'] == 'registered':
            model = model.filter(user__isnull=False)
        if filters['type'] == 'hidden':
            model = model.filter(hidden=True)
        if filters['type'] == 'guest':
            model = model.filter(user__isnull=True)
        if filters['type'] == 'crawler':
            model = model.filter(crawler__isnull=False)
        return model
    
    def prefetch_related(self, items):
        return items.prefetch_related('user')
    
    def select_items(self, items):
        return items.filter(matched=1).filter(admin=0)