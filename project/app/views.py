from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User

from .models import JobDescription, Resume, MatchResult
from .serializers import (
    RegisterSerializer,
    JobDescriptionSerializer,
    ResumeUploadSerializer,
    MatchRequestSerializer,
)
from app.services import get_similarity_from_hf


# =========================
# AUTH
# =========================

class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


# =========================
# JOB DESCRIPTION
# =========================

class JobDescriptionCreateView(CreateAPIView):
    queryset = JobDescription.objects.all()
    serializer_class = JobDescriptionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class JobDescriptionListView(ListAPIView):
    serializer_class = JobDescriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return JobDescription.objects.filter(user=self.request.user)


# =========================
# RESUME
# =========================

class ResumeUploadView(CreateAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeUploadSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        resume_file = self.request.FILES.get("resume_file")

        from .utils.pdf_extractor import (
            extract_text_from_pdf,
            extract_relevant_resume_text,
        )

        full_text = extract_text_from_pdf(resume_file)
        clean_text = extract_relevant_resume_text(full_text)

        serializer.save(
            user=self.request.user,
            text=clean_text,
        )


class ResumeListView(ListAPIView):
    serializer_class = ResumeUploadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)


# =========================
# MATCH
# =========================

class MatchResumeView(CreateAPIView):
    queryset = MatchResult.objects.all()
    serializer_class = MatchRequestSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        job = JobDescription.objects.get(
            id=serializer.validated_data["job_id"]
        )
        resume = Resume.objects.get(
            id=serializer.validated_data["resume_id"]
        )

        # 🔥 HF SPACE CALL
        score = get_similarity_from_hf(
            resume.text,
            job.job_description
        )

        MatchResult.objects.create(
            job=job,
            resume=resume,
            score=score,
        )

        score_percent = round(score * 100, 2)

        if score >= 0.75:
            verdict = "Strong Match"
        elif score >= 0.50:
            verdict = "Moderate Match"
        else:
            verdict = "Low Match"

        return Response(
            {
                "job": job.job_title,
                "candidate": resume.candidate_name,
                "match_score_percent": score_percent,
                "verdict": verdict,
            },
            status=status.HTTP_201_CREATED,
        )


# =========================
# HISTORY
# =========================

class MatchHistoryView(ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        matches = MatchResult.objects.filter(
            job__user=request.user
        ).select_related("job", "resume")

        data = []
        for m in matches:
            score_percent = round(m.score * 100, 2)

            if m.score >= 0.75:
                verdict = "Strong Match"
            elif m.score >= 0.5:
                verdict = "Moderate Match"
            else:
                verdict = "Low Match"

            data.append({
                "id": m.id,
                "job_title": m.job.job_title,
                "candidate_name": m.resume.candidate_name,
                "score_percent": score_percent,
                "verdict": verdict,
                "created_at": m.created_at,
            })

        return Response(data)