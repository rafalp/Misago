from django.http import Http404, HttpResponse


def google_site_verification(request, token):
    if token != request.settings.google_site_verification:
        raise Http404()

    return HttpResponse(f"google-site-verification: google{token}.html")
