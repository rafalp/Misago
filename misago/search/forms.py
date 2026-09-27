import re

from django import forms
from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.utils.translation import pgettext_lazy

from ..categories.display import get_categories_with_branches
from ..categories.proxy import CategoryProxy
from ..users.fields import UserMultipleChoiceField
from .categories import get_searchable_category_ids
from .enums import SearchMode, SearchSort
from .hooks import clean_search_query_hook
from .query import normalize_quotes, parse_search_query
from .validators import (
    validate_search_query,
    validate_search_query_length,
    validate_search_query_term_length,
)

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
    query = forms.CharField()
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

        self.setup_query_field()
        self.setup_users_field()

    def setup_query_field(self):
        field = self.fields["query"]
        field.max_length = self.request.settings.max_search_query_length
        field.min_length = self.request.settings.min_search_term_length

    def setup_users_field(self):
        users_queryset = User.objects
        if not self.request.user.is_misago_admin:
            users_queryset = users_queryset.filter(is_active=True)
        self.fields["users"].queryset = users_queryset

    def clean_query(self):
        query = self.cleaned_data["query"]

        return clean_search_query(
            query,
            max_length=self.request.settings.max_search_query_length,
            min_term_length=self.request.settings.min_search_term_length,
            request=self.request,
        )

    def clean(self):
        data = super().clean()

        if (
            data.get("date_from")
            and data.get("date_to")
            and data["date_from"] > data["date_to"]
        ):
            data["date_from"], data["date_to"] = data["date_to"], data["date_from"]

        try:
            if query_string := data.get("query"):
                self.search_query = parse_search_query(query_string)
                validate_search_query(self.search_query)
        except forms.ValidationError as error:
            self.add_error("query", error)

        return data


def clean_search_query(
    query: str,
    max_length: int,
    min_term_length: int,
    request: HttpRequest | None = None,
) -> str:
    return clean_search_query_hook(
        _clean_search_query_action,
        query,
        max_length=max_length,
        min_term_length=min_term_length,
        request=request,
    )


def _clean_search_query_action(
    query: str,
    max_length: int,
    min_term_length: int,
    request: HttpRequest | None = None,
) -> str:
    query = re.sub(r"\s+", " ", query)
    query = normalize_quotes(query)
    validate_search_query_length(query, max_length)
    validate_search_query_term_length(query, min_term_length)
    return query


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
    searchable_categories: set[int]
    disabled_categories: set[int]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.searchable_categories = self.get_searchable_categories()
        self.disabled_categories = self.get_disabled_categories()
        self.fields["categories"].choices = self.get_category_choices()

    def get_searchable_categories(self) -> set[int]:
        return get_searchable_category_ids(
            self.request.user_permissions, self.request.categories
        )

    def get_disabled_categories(self) -> set[int]:
        return set(self.request.categories).difference(self.searchable_categories)

    def get_category_choices(self) -> tuple[tuple[int, str]]:
        return tuple(
            (category.id, category.name)
            for category in self.request.categories.values()
            if category.id in self.searchable_categories
        )

    def get_categories_with_branches(self) -> list[tuple[str, CategoryProxy]]:
        categories = self.request.categories.values()
        visible_categories: set[int] = set()

        for category in categories:
            if category.id not in self.disabled_categories:
                if category.parent_id:
                    visible_categories.add(category.parent_id)

                visible_categories.add(category.id)

        return get_categories_with_branches(
            tuple(
                category for category in categories if category.id in visible_categories
            )
        )


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
