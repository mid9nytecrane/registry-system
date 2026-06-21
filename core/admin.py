from django.contrib import admin
from import_export import resources, fields
from import_export.admin import ExportActionMixin, ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget

from .models import PartyMember, PollingStation,ElectoralArea


# ── Resource definitions (controls which fields are exported/imported) ──

class PollingStationResource(resources.ModelResource):
    class Meta:
        model = PollingStation
        fields = ('id', 'name', 'location', 'constituency', 'description', 'created_at')
        export_order = ('id', 'name', 'location', 'constituency', 'description')


class PartyMemberResource(resources.ModelResource):
    # Resolve the polling station FK to a human-readable name on export,
    # and accept a station name or pk on import.
    polling_station = fields.Field(
        column_name='polling_station',
        attribute='polling_station',
        widget=ForeignKeyWidget(PollingStation, field='name'),
    )

    class Meta:
        model = PartyMember
        fields = (
            'id', 'member_id', 'first_name', 'middle_name', 'last_name',
            'gender', 'date_of_birth', 'phone', 'occupation', 'address',
            'ghana_card_id', 'voters_id', 'polling_station', 'date_registered',
        )
        export_order = fields
        import_id_fields = ('member_id',)   # use member_id as the unique key on import


# ── Admin registrations ──

admin.site.register(ElectoralArea)

@admin.register(PollingStation)
class PollingStationAdmin(ImportExportModelAdmin, ExportActionMixin):
    resource_classes = [PollingStationResource]
    list_display  = ('name', 'location', 'constituency', 'member_count', 'created_at')
    search_fields = ('name', 'location', 'constituency')
    ordering      = ('name',)


@admin.register(PartyMember)
class PartyMemberAdmin(ImportExportModelAdmin):
    resource_classes = [PartyMemberResource]
    list_display   = ('member_id', 'first_name', 'last_name', 'gender', 'polling_station', 'date_registered')
    list_filter    = ('gender', 'polling_station', 'date_registered')
    search_fields  = ('first_name', 'last_name', 'member_id', 'phone', 'ghana_card_id', 'voters_id')
    readonly_fields = ('member_id',)
    ordering       = ('-date_registered',)
