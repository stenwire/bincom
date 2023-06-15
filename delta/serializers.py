from rest_framework import serializers
from delta.models import AnnouncedPuResults

class PollingUnitResultSerializer(serializers.Serializer):
    class Meta:
        model = AnnouncedPuResults
        fields = '__all__'
