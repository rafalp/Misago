from typing import Any, Iterable

from django.db.models import Model


class UpdatedObjectWrapper:
    _obj: Model
    _eager_fields: set[str] | None
    _update_fields: set[str]

    __slots__ = ("_obj", "_eager_fields", "_update_fields")

    def __init__(self, obj: Model, eager_fields: Iterable[str] | None = None):
        super().__setattr__("_obj", obj)
        super().__setattr__(
            "_eager_fields", set(eager_fields) if eager_fields else None
        )
        super().__setattr__("_update_fields", set())

    def __getattr__(self, name: str) -> Any:
        if self._eager_fields and name in self._eager_fields:
            self._update_fields.add(name)

        return getattr(self._obj, name)

    def __setattr__(self, name: str, value: Any) -> Any:
        self._update_fields.add(name)
        setattr(self._obj, name, value)
        return value

    def unwrap(self) -> Model:
        return self._obj

    def save(self) -> bool:
        if not self._update_fields:
            return False

        self._obj.save(update_fields=self._update_fields)
        return True
