from django import forms
from rest_framework import serializers

from delta.models import AnnouncedPuResults


class PollingUnitResultSerializer(forms.ModelForm):
    class Meta:
        model = AnnouncedPuResults
        fields = "__all__"
