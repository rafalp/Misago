from django.core.exceptions import ValidationError
from django.db.models import Model
from django.http import HttpRequest, HttpResponse
from django.utils.translation import pgettext

from .base import AdminView


class OrderingView(AdminView):
    def post(self, request: HttpRequest):
        items = {item.pk: item for item in self.get_queryset()}
        try:
            ordered_items = self.get_ordered_items(request, items)
            self.order_items(request, ordered_items)
            return HttpResponse(status=204)
        except ValidationError as error:
            return HttpResponse(error.message, status=400)

    def get_queryset(self):
        return self.get_model().objects.all()

    def get_ordered_items(
        self, request: HttpRequest, items: dict[int, Model]
    ) -> list[Model]:
        items_ordering = request.POST.getlist("item")
        if not items_ordering:
            raise ValidationError(pgettext("admin reorder", "No items sent."))

        ordered_items: dict[int, Model] = {}
        for item_id_str in items_ordering:
            try:
                item_id = int(item_id_str)
            except (TypeError, ValueError):
                raise ValidationError(
                    pgettext("admin reorder", "Invalid item type: %(item)s")
                    % {"item": item_id_str}
                )

            if item_id in ordered_items:
                raise ValidationError(
                    pgettext("admin reorder", "The item is not unique: %(item)s")
                    % {"item": item_id}
                )

            try:
                ordered_items[item_id] = items[item_id]
            except KeyError:
                raise ValidationError(
                    pgettext("admin reorder", "The item does not exist: %(item)s")
                    % {"item": item_id}
                )

        return list(ordered_items.values())

    def order_items(self, request: HttpRequest, items: list[Model]):
        pass
