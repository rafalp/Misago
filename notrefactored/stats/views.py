import math
from datetime import datetime, timedelta
from django.core.urlresolvers import reverse
from django.db import models
from django.shortcuts import redirect
from django.template import RequestContext
from django.utils import timezone
from django.utils.translation import ugettext as _
from misago.forms import FormLayout
from misago.messages import Message
from misago.stats.forms import GenerateStatisticsForm
from misago.views import error404

def form(request):
    """
    Allow admins to generate fancy statistic graphs for different models
    """
    statistics_providers = []
    models_map = {}
    for model in models.get_models():
        try:
            getattr(model.objects, 'filter_stats')
            statistics_providers.append((str(model.__name__).lower(), model.statistics_name))
            models_map[str(model.__name__).lower()] = model
        except AttributeError:
            pass

    if not statistics_providers:
        """
        Something went FUBAR - Misago ships with some stats providers out of box
        If those providers cant be found, this means Misago filesystem is corrupted
        """
        return request.theme.render_to_response('stats/not_available.html',
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
                message = Message(_('Start and end date are same'), type='error')
            elif check_dates(date_start, date_end, form.cleaned_data['stats_precision']):
                message = check_dates(date_start, date_end, form.cleaned_data['stats_precision'])
            else:
                request.messages.set_flash(Message(_('Statistical report has been created.')), 'success', 'admin_stats')
                return redirect(reverse('admin_stats_graph', kwargs={
                                                       'model': form.cleaned_data['provider_model'],
                                                       'date_start': date_start.strftime('%Y-%m-%d'),
                                                       'date_end': date_end.strftime('%Y-%m-%d'),
                                                       'precision': form.cleaned_data['stats_precision']
                                                        }))
        else:
            message = Message(form.non_field_errors()[0], 'error')
    else:
        form = GenerateStatisticsForm(provider_choices=statistics_providers, request=request)

    return request.theme.render_to_response('stats/form.html', {
                                            'form': FormLayout(form),
                                            'message': message,
                                            }, context_instance=RequestContext(request));


def graph(request, model, date_start, date_end, precision):
    """
    Generate fancy graph for model and stuff
    """
    if date_start == date_end:
        # Bad dates
        raise error404()

    # Turn stuff into datetime's
    date_start = datetime.strptime(date_start, '%Y-%m-%d')
    date_end = datetime.strptime(date_end, '%Y-%m-%d')


    statistics_providers = []
    models_map = {}
    for model_obj in models.get_models():
        try:
            getattr(model_obj.objects, 'filter_stats')
            statistics_providers.append((str(model_obj.__name__).lower(), model_obj.statistics_name))
            models_map[str(model_obj.__name__).lower()] = model_obj
        except AttributeError:
            pass

    if not statistics_providers:
        # Like before, q.q on lack of models
        return request.theme.render_to_response('stats/not_available.html',
                                                context_instance=RequestContext(request));

    if not model in models_map or check_dates(date_start, date_end, precision):
        # Bad model name or graph data!
        raise error404()

    form = GenerateStatisticsForm(
                                  provider_choices=statistics_providers,
                                  request=request,
                                  initial={'provider_model': model, 'date_start': date_start, 'date_end': date_end, 'stats_precision': precision})
    return request.theme.render_to_response('stats/graph.html', {
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
        return Message(_('Too many many items to display on graph.'), 'error')
    elif ((precision == 'day' and date_diff / 86400 < 1)
          or (precision == 'week' and date_diff / 604800 < 1)
          or (precision == 'month' and date_diff / 2592000 < 1)
          or (precision == 'year' and date_diff / 31536000 < 1)):
        return Message(_('Too few items to display on graph'), 'error')
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
    for item in model.objects.filter_stats(date_start, date_end).iterator():
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
