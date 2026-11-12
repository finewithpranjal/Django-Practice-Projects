from django.contrib import admin
from uc.models import underconstruction


@admin.register(underconstruction)
class UCAdmin(admin.ModelAdmin):
    list_display = ('id', 'uc_note', 'uc_duration', 'is_under_construction', 'updated_at')

    fields = ('uc_note', 'uc_duration', 'is_under_construction')
