from rest_framework import serializers

from misago.users.models import DataExport


__all__ = ['DataExportSerializer']


class DataExportSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataExport
        fields = [
            'id',
            'status',
            'requested_on',
            'expires_on',
            'export_file',
        ]
