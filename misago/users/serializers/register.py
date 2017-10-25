from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from misago.users import captcha, validators
from misago.users.bans import get_email_ban, get_ip_ban, get_username_ban


UserModel = get_user_model()


__all__ = ['RegisterUserSerializer']


class RegisterUserSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=255,
        validators=[validators.validate_username],
    )
    email = serializers.CharField(
        max_length=255,
        validators=[validators.validate_email],
    )
    password = serializers.CharField(
        max_length=255,
        trim_whitespace=False,
    )

    def validate_username(self, data):
        ban = get_username_ban(data, registration_only=True)
        if ban:
            if ban.user_message:
                raise ValidationError(ban.user_message)
            else:
                raise ValidationError(_("This usernane is not allowed."))
        return data

    def validate_email(self, data):
        ban = get_email_ban(data, registration_only=True)
        if ban:
            if ban.user_message:
                raise ValidationError(ban.user_message)
            else:
                raise ValidationError(_("This e-mail address is not allowed."))
        return data

    def validate(self, data):
        request = self.context['request']

        ban = get_ip_ban(request.user_ip, registration_only=True)
        if ban:
            if ban.user_message:
                raise ValidationError(ban.user_message)
            else:
                raise ValidationError(_("New registrations from this IP address are not allowed."))

        self._added_errors = {}

        try:
            self.full_clean_password(data)
        except ValidationError as e:
            self._added_errors['password'] = [e]

        validators.validate_new_registration(request, self, data)

        if self._added_errors:
            # fail registration with additional errors
            raise serializers.ValidationError(self._added_errors)

        # run test for captcha
        try:
            captcha.test_request(self.context['request'])
        except ValidationError as e:
            raise serializers.ValidationError({'captcha': [e.args[0]]})

        return data

    def full_clean_password(self, data):
        if data.get('password'):
            validate_password(
                data['password'],
                user=UserModel(
                    username=data.get('username'),
                    email=data.get('email'),
                ),
            )

    def add_error(self, field, error):
        """we are using custom implementation so custom validators work"""
        self._added_errors.setdefault(field, []).append(error)
