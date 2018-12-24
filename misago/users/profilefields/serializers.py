from ..permissions import can_edit_profile_details


def serialize_profilefields_data(request, profilefields, user):
    data = {"id": user.pk, "groups": [], "edit": False}

    can_edit = can_edit_profile_details(request.user_acl, user)
    has_editable_fields = False

    for group in profilefields.get_fields_groups():
        group_fields = []
        for field in group["fields"]:
            display_data = field.get_display_data(request, user)
            if display_data:
                group_fields.append(display_data)
            if can_edit and field.is_editable(request, user):
                has_editable_fields = True
        if group_fields:
            data["groups"].append({"name": group["name"], "fields": group_fields})

    data["edit"] = can_edit and has_editable_fields

    return data
