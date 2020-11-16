from django.http import JsonResponse
from rest_framework.decorators import action


@action(methods=["get"], detail=True)
def healthcheck(request):
    return JsonResponse({"status": "OK"})
