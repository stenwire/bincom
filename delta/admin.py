from django.contrib import admin
from delta.models import AnnouncedPuResults

# Register your models here.

class AnnouncedPuResultsAdmin(admin.ModelAdmin):
    list_display = [
    # 'polling_unit_uniqueid',
    'party_abbreviation',
    'party_score',
    'entered_by_user',
    ]



admin.site.register(AnnouncedPuResults, AnnouncedPuResultsAdmin)