from .models import Icon


def icons(request):
    return {"icons": {i.type: i.image.url for i in Icon.objects.all()}}
