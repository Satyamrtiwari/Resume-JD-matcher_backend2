from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404  
from rest_framework.decorators import api_view, permission_classes

from .models import JobDescription, Resume, MatchResult
from .serializers import (
    JobDescriptionSerializer,
    ResumeUploadSerializer,
    MatchRequestSerializer,
)
from app.services import get_similarity_from_hf


# =========================
# JOB DESCRIPTION
# =========================

class JobDescriptionCreateView(CreateAPIView):
    queryset = JobDescription.objects.all()
    serializer_class = JobDescriptionSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(user=user)


class JobDescriptionListView(ListAPIView):
    serializer_class = JobDescriptionSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return JobDescription.objects.all()


class JobDescriptionDeleteView(DestroyAPIView):
    permission_classes = [AllowAny]

    def get_queryset(self):
        return JobDescription.objects.all()


# =========================
# RESUME
# =========================

class ResumeUploadView(CreateAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeUploadSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        resume_file = self.request.FILES.get("resume_file")

        from .utils.pdf_extractor import (
            extract_text_from_pdf,
            extract_relevant_resume_text,
        )

        full_text = extract_text_from_pdf(resume_file)
        clean_text = extract_relevant_resume_text(full_text)

        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(
            user=user,
            text=clean_text,
        )


class ResumeListView(ListAPIView):
    serializer_class = ResumeUploadSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Resume.objects.all()


class ResumeDeleteView(DestroyAPIView):
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Resume.objects.all()

    def perform_destroy(self, instance):
        if instance.resume_file:
            instance.resume_file.delete(save=False)
        instance.delete()


# =========================
# MATCH
# =========================

class MatchResumeView(CreateAPIView):
    queryset = MatchResult.objects.all()
    serializer_class = MatchRequestSerializer
    permission_classes = [AllowAny]

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




@api_view(['GET', 'HEAD'])
@permission_classes([AllowAny])
def health_check(request):
    return Response({"status": "ok"})

