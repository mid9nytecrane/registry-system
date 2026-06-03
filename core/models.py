from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
import uuid



# validation for member_id entry
def validate_member_id(value):
    if value < 10 or value > 10:
        raise ValidationError(f"{value} is either less or more")



class PollingStation(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200, blank=True)
    constituency = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

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
    member_id = models.CharField(max_length=20, unique=True, editable=True, validators=[validate_member_id])

    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    occupation = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=200, blank=True)
    ghana_card_id = models.CharField(max_length=50, blank=True, verbose_name='Ghana Card / Voter ID')

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
