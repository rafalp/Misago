from django.utils.translation import ugettext as _

from rest_framework import serializers

from misago.core.utils import format_plaintext_for_html

from misago.users.models import Ban, BAN_USERNAME, BAN_EMAIL, BAN_IP


class BanMessageSerializer(serializers.ModelSerializer):
    message = serializers.SerializerMethodField()

    class Meta:
        model = Ban
        fields = ('message', 'expires_on')

    def get_message(self, obj):
        message = obj.user_message or _("You are banned.")

        return {
            'plain': message,
            'html': format_plaintext_for_html(message)
        }
