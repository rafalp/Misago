from django.contrib.auth import get_user_model, logout
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext as _
from rest_framework import serializers

from ..online.tracker import clear_tracking
from ..permissions import allow_delete_own_account
from ..validators import validate_email, validate_username

User = get_user_model()

__all__ = [
    "ForumOptionsSerializer",
    "EditSignatureSerializer",
    "ChangeUsernameSerializer",
    "ChangePasswordSerializer",
    "ChangeEmailSerializer",
    "DeleteOwnAccountSerializer",
]


class ForumOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "is_hiding_presence",
            "limits_private_thread_invites_to",
            "subscribe_to_started_threads",
            "subscribe_to_replied_threads",
        ]
        extra_kwargs = {
            "limits_private_thread_invites_to": {"required": True},
            "subscribe_to_started_threads": {"required": True},
            "subscribe_to_replied_threads": {"required": True},
        }


class EditSignatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["signature"]

    def validate(self, data):
        settings = self.context["settings"]
        if len(data.get("signature", "")) > settings.signature_length_max:
            raise serializers.ValidationError(_("Signature is too long."))

        return data


class ChangeUsernameSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200, required=False, allow_blank=True)

    def validate(self, data):
        username = data.get("username")
        if not username:
            raise serializers.ValidationError(_("Enter new username."))

        user = self.context["user"]
        if username == user.username:
            raise serializers.ValidationError(_("New username is same as current one."))

        settings = self.context["settings"]
        validate_username(settings, username)

        return data

    def change_username(self, changed_by):
        user = self.context["user"]
        user.set_username(self.validated_data["username"], changed_by=changed_by)
        user.save(update_fields=["username", "slug"])


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=200, trim_whitespace=False)
    new_password = serializers.CharField(max_length=200, trim_whitespace=False)

    def validate_password(self, value):
        if not self.context["user"].check_password(value):
            raise serializers.ValidationError(_("Entered password is invalid."))
        return value

    def validate_new_password(self, value):
        validate_password(value, user=self.context["user"])
        return value


class ChangeEmailSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=200, trim_whitespace=False)
    new_email = serializers.CharField(max_length=200)

    def validate_password(self, value):
        if not self.context["user"].check_password(value):
            raise serializers.ValidationError(_("Entered password is invalid."))
        return value

    def validate_new_email(self, value):
        if not value:
            raise serializers.ValidationError(
                _("You have to enter new e-mail address.")
            )

        if value.lower() == self.context["user"].email.lower():
            raise serializers.ValidationError(_("New e-mail is same as current one."))

        validate_email(value)

        return value


class DeleteOwnAccountSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=200, trim_whitespace=False)

    def validate_password(self, value):
        if not self.context["user"].check_password(value):
            raise serializers.ValidationError(_("Entered password is invalid."))
        return value

    def mark_account_for_deletion(self, request):
        """
        Deleting user account can be costful, so just mark account for deletion,
        deactivate it and sign user out.
        """
        profile = self.context["user"]
        allow_delete_own_account(request.settings, request.user, profile)

        logout(request)
        clear_tracking(request)

        profile.mark_for_delete()
