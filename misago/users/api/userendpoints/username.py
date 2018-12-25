from django.db import IntegrityError
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.response import Response

from ...namechanges import get_username_options
from ...serializers import ChangeUsernameSerializer


def username_endpoint(request):
    if request.method == "POST":
        return change_username(request)

    options = get_username_options_from_request(request)
    return options_response(options)


def get_username_options_from_request(request):
    return get_username_options(request.settings, request.user, request.user_acl)


def options_response(options):
    if options["next_on"]:
        options["next_on"] = options["next_on"].isoformat()
    return Response(options)


def change_username(request):
    options = get_username_options_from_request(request)
    if not options["changes_left"]:
        return Response(
            {"detail": _("You can't change your username now."), "options": options},
            status=status.HTTP_400_BAD_REQUEST,
        )

    serializer = ChangeUsernameSerializer(
        data=request.data, context={"settings": request.settings, "user": request.user}
    )
    if not serializer.is_valid():
        return Response(
            {"detail": serializer.errors["non_field_errors"][0]},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        serializer.change_username(changed_by=request.user)
        updated_options = get_username_options_from_request(request)
        if updated_options["next_on"]:
            updated_options["next_on"] = updated_options["next_on"].isoformat()

        return Response(
            {
                "username": request.user.username,
                "slug": request.user.slug,
                "options": updated_options,
            }
        )
    except IntegrityError:
        return Response(
            {"detail": _("Error changing username. Please try again.")},
            status=status.HTTP_400_BAD_REQUEST,
        )


def moderate_username_endpoint(request, profile):
    if request.method == "POST":
        serializer = ChangeUsernameSerializer(
            data=request.data, context={"settings": request.settings, "user": profile}
        )

        if not serializer.is_valid():
            return Response(
                {"detail": serializer.errors["non_field_errors"][0]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            serializer.change_username(changed_by=request.user)
            return Response({"username": profile.username, "slug": profile.slug})
        except IntegrityError:
            return Response(
                {"detail": _("Error changing username. Please try again.")},
                status=status.HTTP_400_BAD_REQUEST,
            )

    return Response(
        {
            "length_min": request.settings.username_length_min,
            "length_max": request.settings.username_length_max,
        }
    )
