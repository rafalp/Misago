from django.http import Http404

from ...acl.objectacl import add_acl_to_obj
from ...categories.models import Category
from ...categories.permissions import allow_browse_category, allow_see_category
from ...categories.serializers import CategorySerializer
from ...core.shortcuts import validate_slug
from ...core.viewmodel import ViewModel as BaseViewModel
from ..permissions import allow_use_private_threads

__all__ = ["ThreadsRootCategory", "ThreadsCategory", "PrivateThreadsCategory"]


class ViewModel(BaseViewModel):
    def __init__(self, request, **kwargs):
        self._categories = self.get_categories(request)
        add_acl_to_obj(request.user_acl, self._categories)

        self._model = self.get_category(request, self._categories, **kwargs)

        self._subcategories = list(filter(self._model.has_child, self._categories))
        self._children = list(
            filter(lambda s: s.parent_id == self._model.pk, self._subcategories)
        )

    @property
    def categories(self):
        return self._categories

    @property
    def subcategories(self):
        return self._subcategories

    @property
    def children(self):
        return self._children

    def get_categories(self, request):
        raise NotImplementedError(
            "Category view model has to implement get_categories(request)"
        )

    def get_category(self, request, categories, **kwargs):
        return categories[0]

    def get_frontend_context(self):
        return {"CATEGORIES": BasicCategorySerializer(self._categories, many=True).data}

    def get_template_context(self):
        return {"category": self._model, "subcategories": self._children}


class ThreadsRootCategory(ViewModel):
    def get_categories(self, request):
        return [Category.objects.root_category()] + list(
            Category.objects.all_categories()
            .filter(id__in=request.user_acl["visible_categories"])
            .select_related("parent")
        )


class ThreadsCategory(ThreadsRootCategory):
    @property
    def level(self):
        return self._model.level

    def get_category(self, request, categories, **kwargs):
        for category in categories:
            if category.pk == int(kwargs["pk"]):
                if not category.special_role:
                    # check permissions for non-special categories
                    allow_see_category(request.user_acl, category)
                    allow_browse_category(request.user_acl, category)

                if "slug" in kwargs:
                    validate_slug(category, kwargs["slug"])

                return category
        raise Http404()


class PrivateThreadsCategory(ViewModel):
    def get_categories(self, request):
        return [Category.objects.private_threads()]

    def get_category(self, request, categories, **kwargs):
        allow_use_private_threads(request.user_acl)

        return categories[0]


BasicCategorySerializer = CategorySerializer.subset_fields(
    "id",
    "parent",
    "name",
    "description",
    "is_closed",
    "css_class",
    "level",
    "lft",
    "rght",
    "is_read",
    "url",
)
