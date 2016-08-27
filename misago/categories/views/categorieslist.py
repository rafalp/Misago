from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..serializers import CategorySerializer
from ..utils import get_categories_tree


def categories(request):
    categories_tree = get_categories_tree(request.user)

    request.frontend_context['CATEGORIES'] = CategorySerializer(
        categories_tree, many=True).data
    request.frontend_context['CATEGORIES_API'] = reverse(
        'misago:api:categories')

    return render(request, 'misago/categories/list.html', {
        'categories': categories_tree,
    })


@api_view()
def api(request):
    categories_tree = get_categories_tree(request.user)
    return Response(CategorySerializer(categories_tree, many=True).data)
