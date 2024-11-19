from django.db import models


class InterviewRatingSheet(models.Model):
    name = models.CharField(max_length=200, default="MySheet")
    interview = models.ForeignKey(Interview, null=True, on_delete=models.CASCADE)
    round_name = models.OneToOneField(Round, null=True, on_delete=models.CASCADE)
    comment = models.TextField(default="", null=True)

    def __str__(self):  # __unicode__ on Python 2
        return self.name


class RatingAspect(models.Model):
    name = models.CharField(max_length=100)
    comment = models.TextField(null=True, default="", blank=True)
    interview_rating_sheet = models.ForeignKey(
        InterviewRatingSheet, on_delete=models.CASCADE
    )
    points = models.PositiveIntegerField(default=0)
    expected_points = models.PositiveIntegerField(default=0)

    def __str__(self):  # __unicode__ on Python 2
        return self.name


class RatingSheet(models.Model):
    name = models.CharField(max_length=100)
    rate_min = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    rate_max = models.IntegerField(default=6, validators=[MaxValueValidator(100)])

    def __str__(self):  # __unicode__ on Python 2
        return self.name


class Aspect(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, default="")
    rating_sheet = models.ForeignKey(RatingSheet, on_delete=models.CASCADE)
    expected_rate = models.PositiveIntegerField(default=1)

    def __str__(self):  # __unicode__ on Python 2
        return self.name
