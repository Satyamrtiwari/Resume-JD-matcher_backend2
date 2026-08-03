from django.urls import path
from .views import (
    JobDescriptionCreateView,
    JobDescriptionListView,
    JobDescriptionDeleteView,
    ResumeUploadView,
    ResumeListView,
    ResumeDeleteView,
    MatchResumeView,
)

urlpatterns = [
    path("jobs/", JobDescriptionCreateView.as_view(), name="job-create"),
    path("jobs/list/", JobDescriptionListView.as_view(), name="job-list"),
    path("jobs/<int:pk>/", JobDescriptionDeleteView.as_view(), name="job-delete"),
    path("resumes/upload/", ResumeUploadView.as_view(), name="upload-resume"),
    path("resumes/list/", ResumeListView.as_view(), name="resume-list"),
    path("resumes/<int:pk>/", ResumeDeleteView.as_view(), name="resume-delete"),
    path("match/", MatchResumeView.as_view(), name="match-resume"),
]
