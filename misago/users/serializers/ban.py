from django.utils.translation import ugettext as _

from rest_framework import serializers

from misago.core.utils import format_plaintext_for_html

from misago.users.models import Ban, BAN_IP


__all__ = ['BanMessageSerializer']


class BanMessageSerializer(serializers.ModelSerializer):
    message = serializers.SerializerMethodField()

    class Meta:
        model = Ban
        fields = ('message', 'expires_on')

    def get_message(self, obj):
        if obj.user_message:
            message = obj.user_message
        elif obj.check_type == BAN_IP:
            message = _("Your IP address is banned.")
        else:
            message = _("You are banned.")

        return {
            'plain': message,
            'html': format_plaintext_for_html(message)
        }
