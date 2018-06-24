from rest_framework import serializers

from misago.users.models import DataDownload


__all__ = ['DataDownloadSerializer']


class DataDownloadSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataDownload
        fields = [
            'id',
            'status',
            'requested_on',
            'expires_on',
            'file',
        ]
