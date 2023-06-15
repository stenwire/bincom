from rest_framework import serializers
from delta.models import AnnouncedPuResults
from django import forms

class PollingUnitResultSerializer(forms.ModelForm):
    class Meta:
        model = AnnouncedPuResults
        fields = '__all__'
