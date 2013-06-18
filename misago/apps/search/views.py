from django.template import RequestContext
from haystack.query import RelatedSearchQuerySet
from misago.models import Post

def do_search(request):
    query = request.POST.get('search_query')
    sqs = RelatedSearchQuerySet().auto_query(query).order_by('-id').load_all()
    sqs = sqs.load_all_queryset(Post, Post.objects.all().select_related('thread', 'forum'))

    return request.theme.render_to_response('search/results.html',
                                            {
                                             'search_phrase': query,
                                             'results': sqs,
                                            },
                                            context_instance=RequestContext(request))


def show_sesults(request):
    pass