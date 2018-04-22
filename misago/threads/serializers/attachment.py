from rest_framework import serializers

from django.template.defaultfilters import filesizeformat
from django.urls import reverse
from django.utils.translation import ugettext as _

from misago.threads.models import Attachment, AttachmentType


IMAGE_EXTENSIONS = ('jpg', 'jpeg', 'png', 'gif')


class AttachmentSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    filetype = serializers.SerializerMethodField()
    uploader_ip = serializers.SerializerMethodField()
    has_thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = Attachment
        fields = [
            'id',
            'secret',
            'filetype',
            'post',
            'uploaded_on',
            'uploader_name',
            'uploader_ip',
            'filename',
            'size',
            'is_image',
            'has_thumbnail',
        ]

    def get_filetype(self, obj):
        return obj.filetype.name

    def get_uploader_ip(self, obj):
        user = self.context.get('user')
        if user and user.acl_cache['can_see_users_ips']:
            return obj.uploader_ip
        else:
            return None

    def get_has_thumbnail(self, obj):
        return bool(obj.thumbnail)


class NewAttachmentSerializer(serializers.Serializer):
    upload = serializers.FileField()

    def validate_upload(self, upload):
        user = self.context['request'].user
        user_roles = set(r.pk for r in user.get_roles())
        max_attachment_size = user.acl_cache['max_attachment_size']
        
        self.filetype = self.validate_filetype(upload, user_roles)
        self.validate_filesize(upload, self.filetype, max_attachment_size)

        return upload

    def validate_filetype(self, upload, user_roles):
        filename = upload.name.strip().lower()

        queryset = AttachmentType.objects.filter(status=AttachmentType.ENABLED)
        for filetype in queryset.prefetch_related('limit_uploads_to'):
            for extension in filetype.extensions_list:
                if filename.endswith('.%s' % extension):
                    break
            else:
                continue

            if filetype.mimetypes_list and upload.content_type not in filetype.mimetypes_list:
                continue

            if filetype.limit_uploads_to.exists():
                allowed_roles = set(r.pk for r in filetype.limit_uploads_to.all())
                if not user_roles & allowed_roles:
                    continue

            return filetype

        raise serializers.ValidationError(_("You can't upload files of this type."))

    def validate_filesize(self, upload, filetype, hard_limit):
        if upload.size > hard_limit * 1024:
            message = _("You can't upload files larger than %(limit)s (your file has %(upload)s).")
            raise serializers.ValidationError(
                message % {
                    'upload': filesizeformat(upload.size).rstrip('.0'),
                    'limit': filesizeformat(hard_limit * 1024).rstrip('.0'),
                }
            )

        if filetype.size_limit and upload.size > filetype.size_limit * 1024:
            message = _(
                "You can't upload files of this type larger than %(limit)s (your file has %(upload)s)."
            )
            raise serializers.ValidationError(
                message % {
                    'upload': filesizeformat(upload.size).rstrip('.0'),
                    'limit': filesizeformat(filetype.size_limit * 1024).rstrip('.0'),
                }
            )

    def is_upload_image(self, upload):
        filename = upload.name.strip().lower()

        for extension in IMAGE_EXTENSIONS:
            if filename.endswith('.%s' % extension):
                return True
        return False

    def save(self):
        request = self.context['request']
        upload = self.validated_data['upload']

        self.instance = Attachment(
            secret=Attachment.generate_new_secret(),
            filetype=self.filetype,
            size=upload.size,
            uploader=request.user,
            uploader_name=request.user.username,
            uploader_slug=request.user.slug,
            uploader_ip=request.user_ip,
            filename=upload.name,
        )

        if self.is_upload_image(upload):
            try:
                self.instance.set_image(upload)
            except IOError:
                raise serializers.ValidationError({
                    'upload': [_("Uploaded image was corrupted or invalid.")],
                })
        else:
            self.instance.set_file(upload)

        self.instance.save()
        return self.instance