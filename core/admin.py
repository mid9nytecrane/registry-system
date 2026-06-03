from django.contrib import admin
from .models import PartyMember, PollingStation


@admin.register(PollingStation)
class PollingStationAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'constituency', 'member_count')
    search_fields = ('name', 'location', 'constituency')


@admin.register(PartyMember)
class PartyMemberAdmin(admin.ModelAdmin):
    list_display = ('member_id', 'first_name', 'last_name', 'gender', 'polling_station', 'date_registered')
    list_filter = ('gender', 'polling_station', 'date_registered')
    search_fields = ('first_name', 'last_name', 'member_id', 'phone', 'ghana_card_id')
    readonly_fields = ('member_id',)
