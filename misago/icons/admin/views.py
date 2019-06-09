from django.shortcuts import redirect

from ...admin.views import render
from ..models import Icon
from .forms import IconsForm


def icons_admin(request):
    form = IconsForm()
    if request.method == "POST":
        form = IconsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("misago:admin:settings:icons:index")
    return render(request, "misago/admin/icons.html", {"form": form})
