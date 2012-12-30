from django.http import HttpResponse
from misago.markdown import post_markdown

def preview(request):
    if request.POST.get('raw'):
        return HttpResponse(post_markdown(request, request.POST.get('raw')))
    return HttpResponse('')