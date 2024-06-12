from dataclasses import dataclass
from functools import cached_property
from typing import TYPE_CHECKING, Any, TypedDict, Sequence

from django.conf import settings
from django.forms import Field
from django.http import HttpRequest
from django.utils.module_loading import import_string

from ..users.profilefields.basefields import ProfileField

if TYPE_CHECKING:
    from ..users.models import User


class ProfileFieldsetSetting(TypedDict):
    name: str
    fields: Sequence[str]


class FormDataFieldset(TypedDict):
    name: str
    fields: list[str]


@dataclass(frozen=True)
class FormData:
    fieldsets: list[FormDataFieldset]
    fields: dict[str, Field]
    profile_fields: dict[str, ProfileField]

    def clean_data(
        self, field: str, data: Any, request: HttpRequest, user: "User"
    ) -> Any:
        return self.profile_fields[field].clean(request, user, data)


class ProfileFieldsLoader:
    fieldsets: Sequence[ProfileFieldsetSetting]

    def __init__(self, fieldsets: Sequence[ProfileFieldsetSetting]):
        self.fieldsets = fieldsets

    @cached_property
    def profile_fields(self) -> dict[str, ProfileField]:
        fields: dict[str, ProfileField] = {}

        for fieldset in self.fieldsets:
            for field_path in fieldset["fields"]:
                if field_path not in fields:
                    fields[field_path] = import_string(field_path)()

        return fields

    @cached_property
    def fields_dict(self) -> dict[str, ProfileField]:
        fields: dict[str, ProfileField] = {}
        for field in self.profile_fields.values():
            fields[field.fieldname] = field
        return fields

    def get_form_data(self, request: HttpRequest, user: "User") -> FormData | None:
        profile_fields = dict(self.profile_fields)

        fieldsets: list[FormDataFieldset] = []
        fields: dict[str, Field] = {}
        form_data_profile_fields: dict[str, ProfileField] = {}

        for fieldset in self.fieldsets:
            fieldset_fields: dict[str, Field] = {}
            for field_path in fieldset["fields"]:
                profile_field = profile_fields[field_path]
                if profile_field.readonly:
                    continue

                form_field = profile_field.get_form_field(request, user)
                if not form_field:
                    continue

                fieldset_fields[profile_field.fieldname] = form_field
                form_data_profile_fields[profile_field.fieldname] = profile_field

            if fieldset_fields:
                fieldsets.append(
                    FormDataFieldset(
                        name=fieldset["name"],
                        fields=list(fieldset_fields),
                    )
                )

                fields.update(fieldset_fields)

        if fieldsets and fields:
            return FormData(
                fieldsets=fieldsets,
                fields=fields,
                profile_fields=form_data_profile_fields,
            )

        return None


profile_fields = ProfileFieldsLoader(settings.MISAGO_PROFILE_FIELDS)
