from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import reverse
import Evaluator.views as views

app_name = 'Evaluator'

urlpatterns = [
    path(r"", views.index, name="index"),
    # path(r'login', login, {'template_name': 'login.html'}),
    path(r"login", views.user_login, name="login_users"),
    path(r"logout", LogoutView.as_view(), {"template_name": "logout.html"}),
    path(r"profile", views.profile, name="profile"),
    path(r"register", views.register, name="register"),
    path(r"profile/edit", views.edit_profile, name="edit_profile"),
    path(r"profile/password", views.change_password, name="change_password"),
    path(r"userDetails/<int:user_pk>", views.get_details_user, name="user_details"),
    # Question URLs
    path(r"questions", views.all_questions, name="question_list"),
    path(
        r"question/details/<int:question_id>",
        views.question_details,
        name="question_details",
    ),
    path(r"addQuestion", views.create_question, name="add_question"),
    path(r"editQuestion/<int:que_pk>", views.edit_question, name="edit_question"),
    # Interview URLs
    path(r"addInterview", views.add_interview, name="add_interview"),
    path(r"allInterview", views.all_interviews, name="all_interview"),
    path(
        r"detailInterview/<int:interview_pk>",
        views.interviews_details,
        name="interview_details",
    ),
    path(
        r"editInterview/<int:interview_pk>",
        views.edit_interview,
        name="edit_interview",
    ),
    path(r"calendar/<int:year>/<int:month>", views.calendar, name="calendar"),
    path(
        r"allInterview/onDate/<int:year>/<int:month>/<int:day>",
        views.get_interviews_by_date,
        name="interviewsbydate",
    ),
    # Candidate URLS
    path(
        r"candidateDetails/<int:candidate_pk>",
        views.candi_details,
        name="candi_details",
    ),
    path(r"addCandidate", views.add_candidate, name="add_candidate"),
    path(
        r"editCandidate/<int:candidate_pk>",
        views.edit_candidate,
        name="edit_candidate",
    ),
    path(r"allCandidates", views.all_candidates, name="all_candidates"),
    path(r"bulkCreateCandis", views.bulk_upload_candis, name="bulk_upload_candis"),
    # Exam URLs
    path(r"Exams", views.exams, name="allexams"),
    # path(r'addexam', views.create_exam, name="createExam"),
    # path(r'exam/(?P<exam_pk>)', views.exam_details, name='examDetails'),
    path(r"examPreface", views.exam_launch_page, name="examLaunch"),
    # Question Set URLs
    path(r"questionSets", views.get_question_sets, name="allQueSets"),
    path(r"addQuestionSet", views.create_question_set, name="createQuestionSet"),
    path(
        r"qset/<int:qset_pk>",
        views.question_set_details,
        name="question_set_details",
    ),
    # Vendor URLs
    path(r"allVendors", views.allVendors, name="allVendors"),
    path(
        r"vendorDetails/<int:vendor_pk>",
        views.vendor_details,
        name="vendor_details",
    ),
    # Rating Sheet
    path(
        r"addRating/interview/<int:interview_pk>/round/<int:round_pk>",
        views.add_ratings,
        name="addRating",
    ),
    path(
        r"ratingDetails/<int:rating_pk>",
        views.rating_details,
        name="rating_details",
    ),
    path(r"sitesearch", views.search_all, name="globalsearch"),
    # Job Openings
    path(r"allOpenings", views.all_openings, name="allOpenings"),
    path(r"addJobOpening", views.create_opening, name="create_opening"),
    path(
        r"editJobOpening/<int:opening_pk>",
        views.edit_job_opening,
        name="edit_job_opening",
    ),
]
