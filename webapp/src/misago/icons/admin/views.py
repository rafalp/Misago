from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext as _

from ...admin.views import render
from ..models import Icon
from .forms import IconsForm


def icons_admin(request):
    form = IconsForm()
    if request.method == "POST":
        form = IconsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            messages.success(request, _("Icons have been updated."))
            return redirect("misago:admin:settings:icons:index")

    return render(
        request, "misago/admin/icons.html", {"form": form, "icons": get_icons()}
    )


def get_icons():
    return {i.type: i for i in Icon.objects.all()}
