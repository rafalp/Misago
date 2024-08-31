from django.core.exceptions import PermissionDenied
from django.core.paginator import EmptyPage, InvalidPage
from django.db.models import Q
from django.http import Http404
from django.utils.translation import pgettext, pgettext_lazy

from ...acl.objectacl import add_acl_to_obj
from ...core.cursorpagination import get_page
from ...notifications.models import WatchedThread
from ...notifications.threads import get_watched_threads
from ..models import Post, Thread
from ..participants import make_participants_aware
from ..permissions import exclude_invisible_posts, exclude_invisible_threads
from ..serializers import ThreadsListSerializer
from ..utils import add_categories_to_items

__all__ = ["ForumThreads", "PrivateThreads", "filter_read_threads_queryset"]

LISTS_NAMES = {
    "all": None,
    "my": pgettext_lazy("threads list", "Your threads"),
    "new": pgettext_lazy("threads list", "New threads"),
    "unread": pgettext_lazy("threads list", "Unread threads"),
    "watched": pgettext_lazy("threads list", "Watched threads"),
    "unapproved": pgettext_lazy("threads list", "Unapproved content"),
}

LIST_DENIED_MESSAGES = {
    "my": pgettext_lazy(
        "threads list",
        "You have to sign in to see list of threads that you have started.",
    ),
    "new": pgettext_lazy(
        "threads list",
        "You have to sign in to see list of threads you haven't read.",
    ),
    "unread": pgettext_lazy(
        "threads list",
        "You have to sign in to see list of threads with new replies.",
    ),
    "watched": pgettext_lazy(
        "threads list",
        "You have to sign in to see list of threads you are watching.",
    ),
    "unapproved": pgettext_lazy(
        "threads list",
        "You have to sign in to see list of threads with unapproved posts.",
    ),
}


class ViewModel:
    def __init__(self, request, category, list_type, start=0):
        self.request = request

        self.allow_see_list(request, category, list_type)

        category_model = category.unwrap()

        base_queryset = self.get_base_queryset(request, category.categories, list_type)
        base_queryset = base_queryset.select_related("starter", "last_poster")

        threads_categories = [category_model] + category.subcategories

        threads_queryset = self.get_remaining_threads_queryset(
            base_queryset, category_model, threads_categories
        )

        try:
            list_page = get_page(
                threads_queryset,
                "-last_post_id",
                request.settings.threads_per_page,
                start,
            )
        except (EmptyPage, InvalidPage):
            raise Http404()

        if list_page.first:
            pinned_threads = list(
                self.get_pinned_threads(
                    base_queryset, category_model, threads_categories
                )
            )
            threads = list(pinned_threads) + list(list_page.object_list)
        else:
            threads = list(list_page.object_list)

        add_categories_to_items(category_model, category.categories, threads)
        add_acl_to_obj(request.user_acl, threads)

        if list_type == "watched" and request.user.is_authenticated:
            self.watched_threads = get_watched_threads(request.user, threads)
        else:
            self.watched_threads = {}

        if list_type in ("new", "unread"):
            # we already know all threads on list are unread
            for thread in threads:
                thread.is_read = False
                thread.is_new = True
        else:
            for thread in threads:
                thread.is_read = True
                thread.is_new = False

        self.filter_threads(request, threads)

        # set state on object for easy access from hooks
        self.category = category
        self.threads = threads
        self.list_type = list_type
        self.list_page = list_page

    def allow_see_list(self, request, category, list_type):
        if list_type not in LISTS_NAMES:
            raise Http404()

        if request.user.is_anonymous:
            if list_type in LIST_DENIED_MESSAGES:
                raise PermissionDenied(LIST_DENIED_MESSAGES[list_type])
        else:
            has_permission = request.user_acl["can_see_unapproved_content_lists"]
            if list_type == "unapproved" and not has_permission:
                raise PermissionDenied(
                    pgettext(
                        "threads list",
                        "You don't have permission to see unapproved content lists.",
                    )
                )

    def get_list_name(self, list_type):
        return LISTS_NAMES[list_type]

    def get_base_queryset(self, request, threads_categories, list_type):
        return get_threads_queryset(request, threads_categories, list_type).order_by(
            "-last_post_id"
        )

    def get_pinned_threads(self, queryset, category, threads_categories):
        return []

    def get_remaining_threads_queryset(self, queryset, category, threads_categories):
        return []

    def filter_threads(self, request, threads):
        pass  # hook for custom thread types to add features to extend threads

    def get_frontend_context(self):
        return {
            "THREADS": {
                "results": ThreadsListSerializer(
                    self.threads,
                    many=True,
                    context={
                        "settings": self.request.settings,
                        "watched_threads": self.watched_threads,
                    },
                ).data,
                "subcategories": [c.pk for c in self.category.children],
                "next": self.list_page.next,
            }
        }

    def get_template_context(self):
        return {
            "list_name": self.get_list_name(self.list_type),
            "list_type": self.list_type,
            "list_page": self.list_page,
            "threads": self.threads,
        }


class ForumThreads(ViewModel):
    def get_pinned_threads(self, queryset, category, threads_categories):
        if category.level:
            return list(queryset.filter(weight=2)) + list(
                queryset.filter(weight=1, category__in=threads_categories)
            )
        return queryset.filter(weight=2)

    def get_remaining_threads_queryset(self, queryset, category, threads_categories):
        if category.level:
            return queryset.filter(weight=0, category__in=threads_categories)
        return queryset.filter(weight__lt=2, category__in=threads_categories)


class PrivateThreads(ViewModel):
    def get_base_queryset(self, request, threads_categories, list_type):
        queryset = super().get_base_queryset(request, threads_categories, list_type)

        # limit queryset to threads we are participant of
        participated_threads = request.user.threadparticipant_set.values("thread_id")

        if request.user_acl["can_moderate_private_threads"]:
            queryset = queryset.filter(
                Q(id__in=participated_threads) | Q(has_reported_posts=True)
            )
        else:
            queryset = queryset.filter(id__in=participated_threads)

        return queryset

    def get_remaining_threads_queryset(self, queryset, category, threads_categories):
        return queryset.filter(category__in=threads_categories)

    def filter_threads(self, request, threads):
        make_participants_aware(request.user, threads)


def get_threads_queryset(request, categories, list_type):
    queryset = exclude_invisible_threads(request.user_acl, categories, Thread.objects)
    if list_type == "all":
        return queryset
    return filter_threads_queryset(request, categories, list_type, queryset)


def filter_threads_queryset(request, categories, list_type, queryset):
    if list_type == "my":
        return queryset.filter(starter=request.user)
    if list_type == "watched":
        watched_threads = WatchedThread.objects.filter(user=request.user).values(
            "thread_id"
        )
        return queryset.filter(id__in=watched_threads)
    if list_type == "unapproved":
        return queryset.filter(has_unapproved_posts=True)
    if list_type in ("new", "unread"):
        return filter_read_threads_queryset(request, categories, list_type, queryset)
    return queryset


def filter_read_threads_queryset(request, categories, list_type, queryset):
    # grab cutoffs for categories
    cutoff_date = get_cutoff_date(request.settings, request.user)

    visible_posts = Post.objects.filter(posted_on__gt=cutoff_date)
    visible_posts = exclude_invisible_posts(request.user_acl, categories, visible_posts)

    queryset = queryset.filter(id__in=visible_posts.distinct().values("thread"))

    read_posts = visible_posts.filter(id__in=request.user.postread_set.values("post"))

    if list_type == "new":
        # new threads have no entry in reads table
        return queryset.exclude(id__in=read_posts.distinct().values("thread"))

    if list_type == "unread":
        # unread threads were read in past but have new posts
        unread_posts = visible_posts.exclude(
            id__in=request.user.postread_set.values("post")
        )
        queryset = queryset.filter(id__in=read_posts.distinct().values("thread"))
        queryset = queryset.filter(id__in=unread_posts.distinct().values("thread"))
        return queryset
