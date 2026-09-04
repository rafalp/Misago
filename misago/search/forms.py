from django import forms
from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.utils.translation import pgettext_lazy

from ..categories.tree import get_category_tree
from ..users.fields import UserMultipleChoiceField
from .enums import SearchMode, SearchSort

User = get_user_model()


class SearchForm(forms.Form):
    scope: str
    name: str
    link_label: str
    template_name: str
    url_name: str
    request: HttpRequest

    def __init__(self, *args, request: HttpRequest, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)


class BaseThreadsSearchForm(SearchForm):
    query = forms.CharField(min_length=3, max_length=255)
    users = UserMultipleChoiceField(max_choices=10, required=False)
    mode = forms.ChoiceField(
        choices=SearchMode.get_choices(),
        initial=SearchMode.THREADS,
        required=False,
        widget=forms.RadioSelect(),
    )
    sort = forms.ChoiceField(
        choices=SearchSort.get_choices(),
        initial=SearchSort.RELEVANCE,
        required=False,
        widget=forms.RadioSelect(),
    )
    date_from = forms.DateField(required=False)
    date_to = forms.DateField(required=False)

    def __init__(self, data: dict | None = None, *args, **kwargs):
        if data:
            data = data.copy()
            data.setdefault("mode", SearchMode.THREADS)
            data.setdefault("sort", SearchSort.RELEVANCE)

        super().__init__(data, *args, **kwargs)

        self.setup_users_field()

    def setup_users_field(self):
        users_queryset = User.objects
        if not self.request.user.is_misago_admin:
            users_queryset = users_queryset.filter(is_active=True)
        self.fields["users"].queryset = users_queryset

    def clean(self):
        data = super().clean()

        if (
            data.get("date_from")
            and data.get("date_to")
            and data["date_from"] > data["date_to"]
        ):
            data["date_from"], data["date_to"] = data["date_to"], data["date_from"]

        return data


class ThreadsSearchForm(BaseThreadsSearchForm):
    scope = "threads"
    name = pgettext_lazy("threads search form name", "Search threads")
    link_label = pgettext_lazy("threads search form name", "Threads")
    template_name = "misago/search/threads/form.html"
    url_name = "misago:threads-search"

    categories = forms.TypedMultipleChoiceField(
        coerce=int,
        required=False,
        widget=forms.CheckboxSelectMultiple(),
    )
    disabled_categories: set[int]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setup_categories_field()

    def setup_categories_field(self):
        request = self.request

        disabled_choices = set()

        self.fields["categories"].choices = tuple(
            (category.id, category.name) for category in request.categories.values()
        )

        self.disabled_categories = disabled_choices

    def get_category_tree(self):
        return get_category_tree(self.request.categories.values())


class PrivateThreadsSearchForm(BaseThreadsSearchForm):
    scope = "private-threads"
    name = pgettext_lazy("private threads search form name", "Search private threads")
    link_label = pgettext_lazy("private threads search form name", "Private threads")
    template_name = "misago/search/private_threads/form.html"
    url_name = "misago:private-threads-search"


class UsersSearchForm(SearchForm):
    scope = "users"
    name = pgettext_lazy("users search form name", "Search users")
    link_label = pgettext_lazy("users search form name", "Users")
    template_name = "misago/search/users/form.html"
    url_name = "misago:users-search"

    query = forms.CharField(min_length=1, max_length=255)
