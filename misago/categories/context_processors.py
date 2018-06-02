from django.db.models import Q

from misago.core.cache import cache

from .serializers import BasicCategorySerializer
from .models import Category


def preload_categories_json(request):
    try:
        user_acl_key = request.user.acl_key
    except AttributeError:
        return {}
        
    cache_key = 'misago_categories_json_{}'.format(user_acl_key)
    categories_json = cache.get(cache_key, 'nada')
    if categories_json == 'nada':
        is_root = Q(level=0)
        is_visible = Q(id__in=request.user.acl_cache['visible_categories'])

        queryset = Category.objects.all_categories(include_root=True)
        queryset = queryset.filter(is_root | is_visible)

        categories_json = BasicCategorySerializer(queryset, many=True).data
        cache.set(cache_key, categories_json, 15 * 60)
    request.frontend_context['store']['categories'] = categories_json
    return {}
