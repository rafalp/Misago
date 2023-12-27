from django.core.exceptions import ValidationError
from django.db.models import Model
from django.http import HttpRequest, HttpResponse
from django.utils.translation import pgettext

from .base import AdminView


class ReorderView(AdminView):
    def post(self, request: HttpRequest):
        items = {item.pk: item for item in self.get_queryset()}
        try:
            ordered_items = self.get_ordered_items(request, items)
            self.reorder_items(request, ordered_items)
            return HttpResponse()
        except ValidationError as error:
            return HttpResponse(str(error))

    def get_queryset(self):
        return self.get_model().objects.all()

    def get_ordered_items(
        self, request: HttpRequest, items: dict[int, Model]
    ) -> list[Model]:
        ordered_items: dict[int, Model] = {}
        for item_id_str in request.POST.getlist("item"):
            try:
                item_id = int(item_id_str)
            except (TypeError, ValueError):
                raise ValidationError(
                    pgettext(
                        "admin reorder", "One or more items were of an invalid type."
                    )
                )

            if item_id in ordered_items:
                raise ValidationError(
                    pgettext("admin reorder", "One or more items were non-unique.")
                )

            try:
                ordered_items[item_id] = items[item_id]
            except KeyError:
                raise ValidationError(
                    pgettext("admin reorder", "One or more items did not exist.")
                )

        return list(ordered_items.values())

    def reorder_items(self, request: HttpRequest, items: list[Model]):
        pass
