from rest_framework import serializers

from django.urls import reverse

from misago.threads.models import Attachment


__all__ = ['AttachmentSerializer']


class AttachmentSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    acl = serializers.SerializerMethodField()
    is_image = serializers.SerializerMethodField()
    filetype = serializers.SerializerMethodField()
    uploader_ip = serializers.SerializerMethodField()

    url = serializers.SerializerMethodField()

    class Meta:
        model = Attachment
        fields = [
            'id',
            'filetype',
            'post',
            'uploaded_on',
            'uploader_name',
            'uploader_ip',
            'filename',
            'size',
            'acl',
            'is_image',
            'url',
        ]

    def get_acl(self, obj):
        try:
            return obj.acl
        except AttributeError:
            return None

    def get_is_image(self, obj):
        return obj.is_image

    def get_filetype(self, obj):
        return obj.filetype.name

    def get_uploader_ip(self, obj):
        if 'user' in self.context and self.context['user'].acl_cache['can_see_users_ips']:
            return obj.uploader_ip
        else:
            return None

    def get_url(self, obj):
        return {
            'index': obj.get_absolute_url(),
            'thumb': obj.get_thumbnail_url(),
            'uploader': self.get_uploader_url(obj),
        }

    def get_uploader_url(self, obj):
        if obj.uploader_id:
            return reverse(
                'misago:user', kwargs={
                    'slug': obj.uploader_slug,
                    'pk': obj.uploader_id,
                }
            )
        else:
            return None
