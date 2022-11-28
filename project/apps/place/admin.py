from django.contrib import admin

from project.apps.place.models import Place


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'deleted_at')
    readonly_fields = ('created_at', 'updated_at')
