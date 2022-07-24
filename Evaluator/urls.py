from django.conf.urls import url
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import reverse
import Evaluator.views as views

app_name = 'Evaluator'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    #url(r'^login/$', login, {'template_name': 'login.html'}),
    url(r'^login/$', views.user_login, name='login_users'),

    url(r'^logout/$', LogoutView.as_view(), {'template_name': 'logout.html'}),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^register/$', views.register, name='register'),
    url(r'^profile/edit/$', views.edit_profile, name='edit_profile'),
    url(r'^profile/password/$', views.change_password, name='change_password'),
    url(r'^userDetails/(?P<user_pk>\d+)/$',
        views.get_details_user, name='user_details'),

    # Question URLs
    url(r'^questions/$', views.all_questions, name='question_list'),
    url(r'^question/details/(?P<question_id>[0-9]+)/$',
        views.question_details, name='question_details'),
    url(r'^addQuestion/$', views.create_question, name='add_question'),
    url(r'^editQuestion/(?P<que_pk>\d+)/$',
        views.edit_question, name='edit_question'),

    # Interview URLs
    url(r'^addInterview/$', views.add_interview, name='add_interview'),
    url(r'^allInterview/$', views.all_interviews, name='all_interview'),
    url(r'^detailInterview/(?P<interview_pk>\d+)/$',
        views.interviews_details, name='interview_details'),
    url(r'^editInterview/(?P<interview_pk>\d+)/$',
        views.edit_interview, name='edit_interview'),
    url(r'^calendar/(?P<year>\d+)/(?P<month>\d+)$',
        views.calendar, name='calendar'),
    url(r'^allInterview/onDate/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})$',
        views.get_interviews_by_date, name='interviewsbydate'),

    # Candidate URLS
    url(r'^candidateDetails/(?P<candidate_pk>\d+)/$',
        views.candi_details, name='candi_details'),
    url(r'^addCandidate/$', views.add_candidate, name='add_candidate'),
    url(r'^editCandidate/(?P<candidate_pk>\d+)/$',
        views.edit_candidate, name='edit_candidate'),
    url(r'^allCandidates/$', views.all_candidates, name='all_candidates'),
    url(r'^bulkCreateCandis/$', views.bulk_upload_candis, name='bulk_upload_candis'),

    # Exam URLs
    url(r'Exams/$', views.exams, name="allexams"),
    #url(r'addexam/$', views.create_exam, name="createExam"),
    #url(r'^exam/(?P<exam_pk>\d+)/$', views.exam_details, name='examDetails'),
    url(r'^examPreface/$', views.exam_launch_page, name='examLaunch'),

    # Question Set URLs
    url(r'questionSets/$', views.get_question_sets, name="allQueSets"),
    url(r'addQuestionSet/$', views.create_question_set, name="createQuestionSet"),
    url(r'^qset/(?P<qset_pk>\d+)/$', views.question_set_details,
        name='question_set_details'),

    # Vendor URLs
    url(r'^allVendors/$', views.allVendors, name="allVendors"),
    url(r'^vendorDetails/(?P<vendor_pk>\d+)/$',
        views.vendor_details, name="vendor_details"),


    # Rating Sheet
    url(r'addRating/interview/(?P<interview_pk>\d+)/round/(?P<round_pk>\d+)/$',
        views.add_ratings, name='addRating'),
    url(r'ratingDetails/(?P<rating_pk>\d+)/$',
        views.rating_details, name='rating_details'),

    url(r'^sitesearch/$', views.search_all, name='globalsearch'),

    # Job Openings
    url(r'^allOpenings/$', views.all_openings, name='allOpenings'),
    url(r'^addJobOpening/$', views.create_opening, name='create_opening'),
    url(r'^editJobOpening/(?P<opening_pk>\d+)/$',
        views.edit_job_opening, name='edit_job_opening'),
]
