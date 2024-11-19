from django.core.validators import RegexValidator
from django.db import models
from django.shortcuts import reverse
from django.utils import timezone


# Create your models here.


class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_validator = RegexValidator(regex="\d+")
    phone_number = models.CharField(
        max_length=20, validators=[contact_validator], null=True
    )
    address = models.TextField()
    type_choices = (
        ("O", "Online"),
        ("R", "Reference"),
        ("RS", "Recruitment Service"),
        ("OT", "Other"),
        ("N", "None"),
    )
    v_type = (
        models.CharField(  # This field can be shown in template as get_status_display
            max_length=2, choices=type_choices, default="N"
        )
    )

    def __str__(self):  # __unicode__ on Python 2
        return self.name

    def get_absolute_url(self):
        return reverse("vendor_details", args=[str(self.id)])


class Candidate(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)

    contact_validator = RegexValidator(regex="\d+")
    contact_primary = models.CharField(
        max_length=20, validators=[contact_validator], null=True
    )
    experience = models.PositiveIntegerField()
    vendor = models.ForeignKey(Vendor, null=True, on_delete=models.CASCADE)
    skill = models.ManyToManyField(Skill, blank=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):  # __unicode__ on Python 2
        return self.name

    def get_absolute_url(self):
        return reverse("Evaluator:candi_details", args=[str(self.id)])
