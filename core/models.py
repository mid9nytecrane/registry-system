from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import uuid



# validation for member_id entry
def validate_member_id(value):
    if len(value) != 10:
        raise ValidationError(
            'Member ID must be exactly 10 characters long',
        )

    if not value.startswith(('C', 'M')):
        raise ValidationError(
            'Member ID must start with a "C" or "M". '
        )
    
# validation for voters id
def validation_voter_id(value):
    if len(value) != 10:
        raise ValidationError(
            'Voters ID must be exactly 10 digits long.'
        )
    
    if not value.isdigit():
        raise ValidationError(
            'Invalid ID. Enter the correct format'
        )

def validation_phone_no(value):
    if len(value) != 10:
        raise ValidationError('Phone Number must be exactly 10 digits.')
    
    if not value.isdigit():
        raise ValidationError('Phone number should be digits only.')
    
    # Correct usage:
    if not (value.startswith('0')):
        raise ValidationError('Phone number must begin with "0".')
    
validation_ghana_card = RegexValidator(
    regex='^GHA-\d{9}-\d$',
    message='Ghana Card must be in the forma GHA-XXXXXXXX-X',
    code='Invalid_ghana_card'
)



class ElectoralArea(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    constituency = models.CharField(max_length=100,blank=True, null=True)
    description = models.TextField(blank=True, null=True)


    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

     
    @property
    def station_count(self):
        return self.stations.count()



class PollingStation(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200, blank=True)
    constituency = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    electoral_area = models.ForeignKey(
        ElectoralArea,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='stations',
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def member_count(self):
        return self.members.count()


class PartyMember(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    # Auto-generated unique member ID
    member_id = models.CharField(
        max_length=10, 
        unique=True, 
        editable=True, 
        validators=[validate_member_id])

    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=10, blank=True, validators=[validation_phone_no])
    occupation = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=200, blank=True)
    ghana_card_id = models.CharField(
        max_length=15,
        blank=True, 
        verbose_name='Ghana Card',
        validators=[validation_ghana_card]

        )
    voters_id = models.CharField(
        max_length=10, 
        blank=True, 
        unique=True,
        verbose_name='Voters ID',
        validators=[validation_voter_id]
        )

    polling_station = models.ForeignKey(
        PollingStation,
        on_delete=models.SET_NULL,
        null=True,
        related_name='members'
    )

    date_registered = models.DateField(default=timezone.now)
    registered_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='registered_members'
    )

    class Meta:
        ordering = ['-date_registered', 'last_name']

    # def save(self, *args, **kwargs):
    #     if not self.member_id:
    #         self.member_id = 'NCA-' + uuid.uuid4().hex[:6].upper()
    #     super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.member_id})"

    def get_gender_display_value(self):
        return dict(self.GENDER_CHOICES).get(self.gender, '—')
