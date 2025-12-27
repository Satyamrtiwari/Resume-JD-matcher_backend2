from django.contrib import admin
from django.urls import path,include
from .serializers import RegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import JobDescriptionListView, RegisterView, JobDescriptionCreateView, ResumeListView, ResumeUploadView, MatchResumeView, MatchHistoryView,LoginView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("jobs/",JobDescriptionCreateView.as_view(),name="job-create"),
    path("jobs/list/", JobDescriptionListView.as_view(),name="job-list"),
    path("resumes/upload/", ResumeUploadView.as_view(), name="upload-resume"),
    path("resumes/list/", ResumeListView.as_view(),name="resume-list"),
    path("match/", MatchResumeView.as_view(), name="match-resume"),
    path("history/", MatchHistoryView.as_view(), name="match-history"),

]
