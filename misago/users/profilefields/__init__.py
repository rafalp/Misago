import copy
import logging

from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.module_loading import import_string
from django.utils.translation import gettext as _

from ...conf import settings

from .basefields import *
from .serializers import serialize_profilefields_data


logger = logging.getLogger("misago.users.ProfileFields")


class ProfileFields:
    def __init__(self, fields_groups):
        self.is_loaded = False

        self.fields_groups = fields_groups
        self.fields_dict = {}

    def load(self):
        self.fields_dict = {}

        fieldnames = {}

        for group in self.fields_groups:
            for field_path in group["fields"]:
                field = import_string(field_path)
                field._field_path = field_path

                if field_path in self.fields_dict:
                    raise ValueError(
                        "%s profile field has been specified twice" % field._field_path
                    )

                if not getattr(field, "fieldname", None):
                    raise ValueError(
                        "%s profile field has to specify fieldname attribute"
                        % field._field_path
                    )

                if field.fieldname in fieldnames:
                    raise ValueError(
                        (
                            '%s profile field defines fieldname "%s" '
                            "that is already in use by the %s"
                        )
                        % (
                            field._field_path,
                            field.fieldname,
                            fieldnames[field.fieldname],
                        )
                    )

                fieldnames[field.fieldname] = field_path
                self.fields_dict[field_path] = field()

        self.is_loaded = True

    def get_fields(self):
        if not self.is_loaded:
            self.load()
        return self.fields_dict.values()

    def get_fields_groups(self):
        if not self.is_loaded:
            self.load()

        groups = []
        for group in self.fields_groups:
            group_dict = {"name": _(group["name"]), "fields": []}

            for field_path in group["fields"]:
                field = self.fields_dict[field_path]
                group_dict["fields"].append(field)

            if group_dict["fields"]:
                groups.append(group_dict)
        return groups

    def add_fields_to_form(self, request, user, form):
        if not self.is_loaded:
            self.load()

        form._profile_fields = []

        for field in self.get_fields():
            if not field.is_editable(request, user):
                continue

            form._profile_fields.append(field.fieldname)
            form.fields[field.fieldname] = field.get_form_field(request, user)

    def add_fields_to_admin_form(self, request, user, form):
        self.add_fields_to_form(request, user, form)

        form._profile_fields_groups = []
        for group in self.fields_groups:
            group_dict = {"name": _(group["name"]), "fields": []}

            for field_path in group["fields"]:
                field = self.fields_dict[field_path]
                if field.fieldname in form._profile_fields:
                    group_dict["fields"].append(field.fieldname)

            if group_dict["fields"]:
                form._profile_fields_groups.append(group_dict)

    def clean_form(self, request, user, form, cleaned_data):
        for field in self.get_fields():
            if field.fieldname not in cleaned_data:
                continue

            try:
                cleaned_data[field.fieldname] = field.clean(
                    request, user, cleaned_data[field.fieldname]
                )
            except ValidationError as e:
                form.add_error(field.fieldname, e)

        return cleaned_data

    def update_user_profile_fields(self, request, user, form):
        old_fields = copy.copy(user.profile_fields or {})

        new_fields = {}
        for fieldname in form._profile_fields:
            if fieldname in form.cleaned_data:
                new_fields[fieldname] = form.cleaned_data[fieldname]
        user.profile_fields = new_fields

        old_fields_reduced = {k: v for k, v in old_fields.items() if v}
        new_fields_reduced = {k: v for k, v in new_fields.items() if v}

        if old_fields_reduced != new_fields_reduced:
            self.log_profile_fields_update(request, user)

    def log_profile_fields_update(self, request, user):
        if request.user == user:
            log_message = "%s edited own profile fields" % user.username
        else:
            log_message = "%s edited %s's (#%s) profile fields" % (
                request.user,
                user.username,
                user.pk,
            )

        logger.info(
            log_message,
            extra={
                "absolute_url": request.build_absolute_uri(
                    reverse(
                        "misago:user-details", kwargs={"slug": user.slug, "pk": user.pk}
                    )
                )
            },
        )

    def search_users(self, criteria, queryset):
        if not self.is_loaded:
            self.load()

        q_obj = None
        for field in self.fields_dict.values():
            q = field.search_users(criteria)
            if q:
                if q_obj:
                    q_obj = q_obj | q
                else:
                    q_obj = q
        if q_obj:
            return queryset.filter(q_obj)

        return queryset


profilefields = ProfileFields(settings.MISAGO_PROFILE_FIELDS)
