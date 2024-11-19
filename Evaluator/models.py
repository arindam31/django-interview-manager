# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from pyexpat import model
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.shortcuts import redirect
from django.utils import timezone
from simple_history.models import HistoricalRecords
from django.shortcuts import reverse
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth

from datetime import datetime
from collections import OrderedDict


class QuestionSet(models.Model):
    name = models.CharField(max_length=200, default='QuestionSet')
    times_taken = models.IntegerField(default=0, editable=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('Evaluator:question_set_details', args=[str(self.id)])


class Interview(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    date = models.DateField()
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    question_set = models.ForeignKey(
        QuestionSet, null=True, blank=True, on_delete=models.CASCADE)
    history = HistoricalRecords()
    status_choices = (
        ('AC', 'Active'),
        ('CN', 'Cancelled'),
        ('FN', 'Finished'),
    )
    status = models.CharField(  # This field can be shown in template as get_status_display
        max_length=2,
        choices=status_choices,
        default='AC'
    )

    # This is to mark if the candidate passed the test.
    result_choices = (
        ('S', 'Selected'),
        ('R', 'Rejected'),
        ('J', 'Joined'),
        ('DNJ', 'Did Not Join'),
        ('TBD', 'Pending'),
    )

    result = models.CharField(  # This field can be shown in template as get_result_display
        max_length=3,
        choices=result_choices,
        default='TBD'
    )

    def __str__(self):  # __unicode__ on Python 2
        return "{0}_{1}_{2}".format(self.candidate, str(self.date), self.position)

    def get_absolute_url(self):
        return reverse('Evaluator:interview_details', args=[str(self.id)])

    @classmethod
    def interviews_today(cls):
        return Interview.objects.filter(date=datetime.today())

    @classmethod
    def all_interviews(cls):
        return Interview.objects.all()

    @classmethod
    def count_interviews_past_30_days(self):
        return self.objects.filter(date__gt=datetime.date.today() - datetime.timedelta(30))

    @classmethod
    def count_all_months_interviews_current_year(self):
        # Below query gives a list of objects which look like this: {'c': 1, 'month': datetime.date(2018, 1, 1)}
        result = self.objects.annotate(month=TruncMonth('date')).values(
            'month').annotate(c=Count('id')).order_by('month')

        d = dict()
        for item in result:
            d[item['month'].month] = item['c']
        for i in range(1, 13):
            if i not in d.keys():
                d[i] = 0

        return d.values()


class Round(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    contact_time = models.TimeField(default=timezone.now)
    assignee = models.ForeignKey(User, on_delete=models.CASCADE)
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    modified_on = models.DateTimeField(default=timezone.now, editable=False)
    comments = models.CharField(
        max_length=300, default='', null=True, blank=True)
    supporting_interviewer = models.ManyToManyField(
        User, blank=True, related_name="supporters")

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        self.modified_on = timezone.now()
        return super(Round, self).save(*args, **kwargs)

    type_choices = (
        ('CV', 'CV Review'),
        ('U', 'Undecided'),
        ('F2F', 'Face to Face'),
        ('SKYPE', 'Skype Call'),
        ('TP', 'Telephonic'),
        ('VC', 'Client Video Call'),
        ('FD', 'Final Discussion'),
        ('HR', 'HR Discussion'),
        ('Other', 'Other Types'),
    )

    round_type = models.CharField(  # This field can be shown in template as get_status_display
        max_length=10,
        choices=type_choices,
        default='U'
    )

    result_choice = (
        ('ADV', 'Advanced'),
        ('RJ', 'Rejected'),
        ('CN', 'Cancelled'),
        ('DNA', 'Did Not Appear'),
        ('DNO', 'Did Not Accept Offer'),
        ('RS', 'Rescheduled'),
        ('W', 'Waiting'),
        ('S', 'Selected'),
        ('OH', 'On Hold'),
    )

    result = models.CharField(  # This field can be shown in template as get_status_display
        max_length=5,
        choices=result_choice,
        default='W'
    )

    def __str__(self):  # __unicode__ on Python 2
        return self.name


class Question(models.Model):
    description = models.CharField('Description', max_length=300)
    difficulty_choice = (
        ('H', 'Hard'),
        ('M', 'Medium'),
        ('E', 'Easy'),
    )

    difficulty = models.CharField(
        max_length=3,
        choices=difficulty_choice,
        default='M'
    )

    skill = models.ForeignKey(Skill, null=True, on_delete=models.CASCADE)
    qset = models.ManyToManyField(QuestionSet)

    def __str__(self):  # __unicode__ on Python 2
        return "{0}".format(self.description)

    def get_absolute_url(self):
        return reverse('Evaluator:question_details', args=[str(self.id)])


class Answer(models.Model):
    """
    Answer's Model, which is used as the answer in Question Model
    """
    detail = models.CharField(max_length=128, verbose_name=u'Answer\'s text')
    question = models.ForeignKey(Question, null=True, on_delete=models.CASCADE)
    correct = models.BooleanField('Correct', default=True)

    def __str__(self):
        return self.detail


class Document(models.Model):
    document = models.FileField(upload_to='resumes/')
    upload_to = models.DateTimeField(
        auto_now_add=True)
    candidate = models.OneToOneField(Candidate, on_delete=models.CASCADE)

    def __str__(self):
        return 'Resume_{}'.format(self.candidate.name)
