from ...admin.views import render
from ..metadata import plugins_metadata


def plugins_list(request):
    return render(
        request,
        "misago/admin/plugins/list.html",
        {"plugins": plugins_metadata.get_metadata().values()},
    )
