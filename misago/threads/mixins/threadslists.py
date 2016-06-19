from datetime import timedelta

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.db.models import F, Q
from django.utils import timezone
from django.utils.translation import ugettext as _

from misago.categories.models import Category

from misago.threads.models import Thread
from misago.threads.permissions import exclude_invisible_threads


class ThreadsListMixin(object):
    def allow_see_list(self, request, category, list_type):
        if request.user.is_anonymous():
            if list_type == 'my':
                raise PermissionDenied(_("You have to sign in to see list of threads that you have started."))

            if list_type == 'new':
                raise PermissionDenied(_("You have to sign in to see list of threads you haven't read."))

            if list_type == 'unread':
                raise PermissionDenied(_("You have to sign in to see list of threads with new replies."))

            if list_type == 'subscribed':
                raise PermissionDenied(_("You have to sign in to see list of threads you are subscribing."))

            if list_type == 'unapproved':
                raise PermissionDenied(_("You have to sign in to see list of threads with unapproved posts."))
        else:
            if list_type == 'unapproved' and not request.user.acl['can_see_unapproved_content_lists']:
                raise PermissionDenied(_("You don't have permission to see unapproved content lists."))

    def get_categories(self, request):
        return [Category.objects.root_category()] + list(
            Category.objects.all_categories().filter(
                id__in=request.user.acl['visible_categories']
            ).select_related('parent'))

    def get_visible_subcategories(self, threads, threads_categories):
        visible_subcategories = []
        for thread in threads:
            if (thread.top_category and thread.category in threads_categories and
                    thread.top_category not in visible_subcategories):
                visible_subcategories.append(thread.top_category)
        return visible_subcategories

    def get_base_queryset(self, request, categories, list_type):
        # [:1] cos we are cutting off root caregory on forum threads list
        # as it includes nedless extra condition to DB filter
        if categories[0].special_role:
            categories = categories[1:]
        queryset = get_threads_queryset(request.user, categories, list_type)
        return queryset.order_by('-last_post_id')


def get_threads_queryset(user, categories, list_type):
    queryset = exclude_invisible_threads(user, categories, Thread.objects)

    if list_type == 'all':
        return queryset
    else:
        return filter_threads_queryset(user, categories, list_type, queryset)


def filter_threads_queryset(user, categories, list_type, queryset):
    if list_type == 'my':
        return queryset.filter(starter=user)
    elif list_type == 'subscribed':
        subscribed_threads = user.subscription_set.values('thread_id')
        return queryset.filter(id__in=subscribed_threads)
    elif list_type == 'unapproved':
        return queryset.filter(has_unapproved_posts=True)
    elif list_type in ('new', 'unread'):
        return filter_read_threads_queryset(user, categories, list_type, queryset)
    else:
        return queryset


def filter_read_threads_queryset(user, categories, list_type, queryset):
    # grab cutoffs for categories
    cutoff_date = timezone.now() - timedelta(
        days=settings.MISAGO_FRESH_CONTENT_PERIOD
    )

    if cutoff_date < user.joined_on:
        cutoff_date = user.joined_on

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
