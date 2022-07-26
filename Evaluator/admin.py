# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Document
from .models import InterviewRatingSheet
from .models import RatingSheet, Aspect, RatingAspect
from .models import JobOpening
from .models import Vendor
from .models import Round
from .models import QuestionSet
from .models import Skill
from .models import Question, Answer
from .models import Interview
from .models import Position
from .models import Candidate
from simple_history.admin import SimpleHistoryAdmin

from django.contrib import admin

admin.autodiscover()
admin.site.enable_nav_sidebar = False

# Register your models here.


class VendorAdmin(admin.ModelAdmin):
    model = Position
    list_display = ('name', 'v_type')


class PositionAdmin(admin.ModelAdmin):
    model = Position
    list_display = ('__str__', 'id_code', 'exp_needed', 'location', 'j_type')


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0


class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['description']
    list_filter = ['difficulty', 'skill']
    list_display = ('description', 'difficulty', 'skill')
    fieldsets = [
        (None,               {'fields': [
         'description', 'difficulty', 'skill', 'qset']}),

    ]
    inlines = [AnswerInline]


class RoundInline(admin.TabularInline):
    model = Round
    extra = 0


class InterviewAdmin(SimpleHistoryAdmin):
    model = Interview
    list_display = ('__str__', 'candidate', 'date',
                    'position', 'status', 'result')
    search_fields = ['candidate__name']
    list_editable = ['status', 'result']
    list_filter = ['status', 'result']
    history_list_display = ["status", "result"]

    inlines = [RoundInline]


class AspectInline(admin.TabularInline):
    model = Aspect
    extra = 0


class RatingAspectInline(admin.TabularInline):
    model = RatingAspect
    extra = 0


class RatingSheetAdmin(admin.ModelAdmin):
    def aspects_count(self, obj):
        return obj.aspect_set.count()

    list_display = ('name', 'rate_min', 'rate_max', 'aspects_count')
    model = RatingSheet
    inlines = [AspectInline]


class InterviewRatingSheetAdmin(admin.ModelAdmin):
    def candidate_name(self, obj):
        return obj.interview.candidate.name

    def aspects_count(self, obj):
        return obj.aspect_set.count()

    model = InterviewRatingSheet

    list_display = ['name', 'round_name', 'candidate_name']
    readonly_fields = ['interview', 'round_name', ]
    inlines = [RatingAspectInline]


class DocumentInline(admin.TabularInline):
    model = Document
    extra = 0


class CandidateAdmin(admin.ModelAdmin):
    model = Candidate
    list_display = ['name', 'position_applied',
                    'created_at', 'vendor', 'candi_resume']
    search_fields = ['name']
    list_filter = ['position_applied']

    inlines = [DocumentInline]

    def candi_resume(self, object):
        return object.document


class JobOpeningAdmin(admin.ModelAdmin):
    model = JobOpening

    list_display = ['__str__', 'position_code', 'no_of_openings', 'posted_on']

    def position_code(self, object):
        return object.position.id_code


admin.site.register(Vendor, VendorAdmin)
admin.site.register(Candidate, CandidateAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(Interview, InterviewAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Skill)
admin.site.register(JobOpening, JobOpeningAdmin)
admin.site.register(QuestionSet)
admin.site.register(RatingSheet, RatingSheetAdmin)
admin.site.register(InterviewRatingSheet, InterviewRatingSheetAdmin)
