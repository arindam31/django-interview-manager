from __future__ import unicode_literals

import csv

from django.shortcuts import render, redirect, reverse
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm
from django.contrib.auth import update_session_auth_hash, authenticate, login
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.functions import TruncMonth
from django.db.models import Sum, Count
from django.template.loader import get_template
from django.template import Context
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from Evaluator import forms
from Evaluator.models import Interview, Question, Candidate, Answer, QuestionSet, Round, Vendor, Skill
from Evaluator.models import Position
from Evaluator.models import JobOpening, Document
from Evaluator.models import RatingAspect, InterviewRatingSheet
from Evaluator.filters import InterviewFilter, CandidateFilter, QuestionFilter

from django.conf import settings

from Evaluator.search import global_search
from Evaluator.mycalendar import InterviewCalendar

import json
import logging
import datetime

# This is to make email mandatory while creating user from admin interface
User._meta.get_field('email').blank = False

# This is to turn ON "is_staff" by default , when a user gets created.
User._meta.get_field('is_staff').default = True

logger = logging.getLogger('mylogs')


def download_csv_report(result, report_name):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s"' % report_name
    writer = csv.writer(response)
    for row in result:
        writer.writerow(row)
    logger.debug('CSV Report generated with name: %s' % report_name)
    return response
