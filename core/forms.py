from django import forms
from .models import PartyMember

# Shared Tailwind classes per widget type
_text_cls = (
    'w-full px-3 py-2.5 text-sm border border-[#95c98d]/50 rounded-lg '
    'focus:outline-none focus:ring-2 focus:ring-[#6aaa64]/40 bg-[#f0f0c8] '
    'transition-all duration-200 hover:border-[#6aaa64] placeholder-[#2d5a27]/30'
)
_select_cls = (
    'w-full px-3 py-2.5 text-sm border border-[#95c98d]/50 rounded-lg '
    'focus:outline-none focus:ring-2 focus:ring-[#6aaa64]/40 bg-[#f0f0c8] '
    'transition-all duration-200 hover:border-[#6aaa64]'
)
_mono_cls = _text_cls + ' font-mono'


class PartyMemberForm(forms.ModelForm):
    class Meta:
        model = PartyMember
        # member_id is auto-generated; registered_by is set by the view
        exclude = [ 'registered_by']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': _text_cls,
                'placeholder': 'e.g. Sheriff',
            }),
            'middle_name': forms.TextInput(attrs={
                'class': _text_cls,
                'placeholder': 'e.g. Shunkpa',
            }),
            'last_name': forms.TextInput(attrs={
                'class': _text_cls,
                'placeholder': 'e.g. Sakara',
            }),
            'gender': forms.Select(attrs={
                'class': _select_cls,
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': _text_cls,
                'type': 'date',
            }),
            'phone': forms.TextInput(attrs={
                'class': _text_cls,
                'placeholder': 'e.g. 0244123456',
                'type': 'tel',
            }),
            'occupation': forms.TextInput(attrs={
                'class': _text_cls,
                'placeholder': 'e.g. Farmer',
            }),
            'address': forms.TextInput(attrs={
                'class': _text_cls,
                'placeholder': 'Area / community / street',
            }),
            'ghana_card_id': forms.TextInput(attrs={
                'class': _mono_cls,
                'placeholder': 'e.g. GHA-000000000-0',
            }),
            'member_id': forms.TextInput(attrs={
                'class': _mono_cls,
                'placeholder': 'e.g. MXXXXXXXXXX',
            }),
            'voters_id': forms.TextInput(attrs={
                'class': _mono_cls,
                'placeholder': 'e.g. XXXXXXXXXXX',
            }),
            'polling_station': forms.Select(attrs={
                'class': _select_cls,
            }),
            'date_registered': forms.DateInput(attrs={
                'class': _text_cls,
                'type': 'date',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make non-critical fields optional at form level
        self.fields['middle_name'].required = False
        self.fields['gender'].required = False
        self.fields['date_of_birth'].required = False
        self.fields['phone'].required = False
        self.fields['occupation'].required = False
        self.fields['address'].required = False
        self.fields['ghana_card_id'].required = False
        self.fields['member_id'].required = True
        self.fields['voters_id'].required = True
        self.fields['date_registered'].required = False
        # Add empty label to the station dropdown
        self.fields['polling_station'].empty_label = 'Select a station…'
