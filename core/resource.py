from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import PartyMember, PollingStation 

class PartyMemberResource(resources.ModelResource):
    polling_station = fields.Field(
        column_name='polling_station',
        attribute='polling_station',
        widget=ForeignKeyWidget(PollingStation, field='name')
    )
    class Meta:
        model = PartyMember
        fields = (
            'id', 'member_id', 'first_name', 'middle_name', 'last_name',
            'gender', 'date_of_birth', 'phone', 'occupation', 'address',
            'ghana_card_id', 'voters_id', 'polling_station', 'date_registered',
        )

        export_order = (
            'first_name', 'middle_name', 'last_name','gender','member_id','voters_id','phone'
        )

        import_id_fields = ['member_id']