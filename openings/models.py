from django.db import models
from django.utils import timezone


class Position(models.Model):
    name = models.CharField(max_length=50)
    id_code = models.CharField(max_length=10)
    years_of_exp_needed = models.PositiveIntegerField(default=0)
    technology = models.TextField(default="")
    location = models.CharField(max_length=100, default="Gotham")
    rating_sheet = models.ForeignKey(RatingSheet, null=True, on_delete=models.CASCADE)
    type_choices = (
        ("P", "Permanent"),
        ("T", "Temporary"),
        ("I", "Intern"),
    )
    j_type = (
        models.CharField(  # This field can be shown in template as get_status_display
            max_length=1, choices=type_choices, default="P"
        )
    )

    def __str__(self):  # __unicode__ on Python 2
        return self.name


class Skill(models.Model):
    name = models.CharField("Name", max_length=20)
    position = models.ManyToManyField(Position)

    def __str__(self):  # __unicode__ on Python 2
        return self.name


class JobOpening(models.Model):
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    no_of_openings = models.PositiveIntegerField(default=1)
    posted_on = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return "Opening_{}".format(self.position.id_code)


class JobApplication(models.Model):
    """This model exists to address the idea:

    - a candidate should be just an independent object. So we isolated him.
    - a candidate might apply for multiple positions.
    - a job application will bring a process in between the candi and following interviews
    - interviews then can be connected to a particular application.
    - an application can be managed independently with different stages and results for the same candidate.
    """

    opening = models.ForeignKey(Position, on_delete=models.CASCADE)
