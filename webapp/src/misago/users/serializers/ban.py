from django.utils.translation import gettext as _
from rest_framework import serializers

from ...core.utils import format_plaintext_for_html
from ..models import Ban

__all__ = ["BanMessageSerializer", "BanDetailsSerializer"]


def serialize_message(message):
    if message:
        return {"plain": message, "html": format_plaintext_for_html(message)}


class BanMessageSerializer(serializers.ModelSerializer):
    message = serializers.SerializerMethodField()

    class Meta:
        model = Ban
        fields = ["message", "expires_on"]

    def get_message(self, obj):
        if obj.user_message:
            message = obj.user_message
        elif obj.check_type == Ban.IP:
            message = _("Your IP address is banned.")
        else:
            message = _("You are banned.")

        return serialize_message(message)


class BanDetailsSerializer(serializers.ModelSerializer):
    user_message = serializers.SerializerMethodField()
    staff_message = serializers.SerializerMethodField()

    class Meta:
        model = Ban
        fields = ["user_message", "staff_message", "expires_on"]

    def get_user_message(self, obj):
        return serialize_message(obj.user_message)

    def get_staff_message(self, obj):
        return serialize_message(obj.staff_message)
