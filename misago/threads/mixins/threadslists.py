from datetime import timedelta

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.db.models import F, Q
from django.utils import timezone
from django.utils.translation import ugettext as _

from misago.categories.models import CATEGORIES_TREE_ID, Category
from misago.categories.permissions import (
    allow_see_category, allow_browse_category)
from misago.core.shortcuts import get_object_or_404, validate_slug
from misago.readtracker import threadstracker

from misago.threads.models import Thread
from misago.threads.permissions import exclude_invisible_threads


def filter_threads_queryset(user, categories, list_type, queryset):
    if list_type == 'my':
        return queryset.filter(starter=user)
    elif list_type == 'subscribed':
        subscribed_threads = user.subscription_set.values('thread_id')
        return queryset.filter(id__in=subscribed_threads)
    else:
        # grab cutoffs for categories
        cutoff_date = timezone.now() - timedelta(
            days=settings.MISAGO_FRESH_CONTENT_PERIOD
        )

        if cutoff_date < user.reads_cutoff:
            cutoff_date = user.reads_cutoff

        categories_dict = {}
        for record in user.categoryread_set.filter(category__in=categories):
            if record.last_read_on > cutoff_date:
                categories_dict[record.category_id] = record.last_read_on

        if list_type == 'new':
            # new threads have no entry in reads table
            # AND were started after cutoff date
            read_threads = user.threadread_set.filter(
                category__in=categories
            ).values('thread_id')

            condition = Q(last_post_on__lte=cutoff_date)
            condition = condition | Q(id__in=read_threads)

            if categories_dict:
                for category_id, category_cutoff in categories_dict.items():
                    condition = condition | Q(
                        category_id=category_id,
                        last_post_on__lte=category_cutoff,
                    )

            return queryset.exclude(condition)
        elif list_type == 'unread':
            # unread threads were read in past but have new posts
            # after cutoff date
            read_threads = user.threadread_set.filter(
                category__in=categories,
                thread__last_post_on__gt=cutoff_date,
                last_read_on__lt=F('thread__last_post_on')
            ).values('thread_id')

            queryset = queryset.filter(id__in=read_threads)

            # unread threads have last reply after read/cutoff date
            if categories_dict:
                conditions = None

                for category_id, category_cutoff in categories_dict.items():
                    condition = Q(
                        category_id=category_id,
                        last_post_on__lte=category_cutoff,
                    )
                    if conditions:
                        conditions = conditions | condition
                    else:
                        conditions = condition

                return queryset.exclude(conditions)
            else:
                return queryset


def get_threads_queryset(user, categories, list_type):
    queryset = exclude_invisible_threads(user, categories, Thread.objects)

    if list_type == 'all':
        return queryset
    else:
        return filter_threads_queryset(user, categories, list_type, queryset)


class ThreadsListMixin(object):
    def allow_see_list(self, request, category, list_type):
        if request.user.is_anonymous():
            if list_type == 'my':
                raise PermissionDenied( _("You have to sign in to see list of "
                                          "threads that you have started."))

            if list_type == 'new':
                raise PermissionDenied(_("You have to sign in to see list of "
                                         "threads you haven't read."))

            if list_type == 'unread':
                raise PermissionDenied(_("You have to sign in to see list of "
                                         "threads with new replies."))

            if list_type == 'subscribed':
                raise PermissionDenied(_("You have to sign in to see list of "
                                         "threads you are subscribing."))

    def get_subcategories(self, request, category):
        if category.is_leaf_node():
            return []

        visible_categories = request.user.acl['visible_categories']
        queryset = category.get_descendants().filter(id__in=visible_categories)
        return list(queryset.order_by('lft'))

    def get_queryset(self, request, categories, list_type):
        # [:1] cos we are cutting off root caregory on forum threads list
        # as it includes nedless extra condition to DB filter
        if categories[0].special_role:
            categories = categories[1:]
        return get_threads_queryset(request.user, categories, list_type)

    def get_extra_context(self, request, category, subcategories, list_type):
        return {
            'is_index': not settings.MISAGO_CATEGORIES_ON_INDEX
        }
