from django.http import Http404

from misago.acl import add_acl
from misago.core.shortcuts import validate_slug

from misago.categories.models import Category
from misago.categories.permissions import allow_see_category, allow_browse_category
from misago.categories.serializers import BasicCategorySerializer


class ViewModel(object):
    def __init__(self, request, **kwargs):
        self.categories = self.get_categories(request)
        map(lambda c: add_acl(request.user, c), self.categories)

        self.category = self.get_category(request, self.categories, **kwargs)
        self.subcategories = filter(self.category.has_child, self.categories)
        self.children = filter(lambda s: s.parent_id == self.category.pk, self.subcategories)

    def get_categories(self, request):
        raise NotImplementedError('Category view model has to implement get_categories(request)')

    def get_category(self, request, categories, **kwargs):
        return categories[0]

    def get_frontend_context(self):
        return {
            'CATEGORIES': BasicCategorySerializer(self.categories, many=True).data
        }

    def get_template_context(self):
        return {
            'category': self.category,
            'subcategories': self.children
        }


class ThreadsRootCategory(ViewModel):
    def get_categories(self, request):
        return [Category.objects.root_category()] + list(
            Category.objects.all_categories().filter(
                id__in=request.user.acl['browseable_categories']
            ).select_related('parent'))


class ThreadsCategory(ThreadsRootCategory):
    @property
    def level(self):
        return self.category.level

    def get_category(self, request, categories, **kwargs):
        for category in categories:
            if category.pk == int(kwargs['pk']):
                if not category.special_role:
                    # don't check permissions for non-special category
                    allow_see_category(request.user, category)
                    allow_browse_category(request.user, category)

                if 'slug' in kwargs:
                    validate_slug(category, kwargs['slug'])

                return category
        raise Http404()


class PrivateThreadsCategory(ViewModel):
    pass
