# serializers.py
from rest_framework import serializers
from .models import JobDescription, Resume, MatchResult


class JobDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobDescription
        fields = ["id", "job_title", "job_description"]


class ResumeUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ["id", "candidate_name", "resume_file"]


class MatchRequestSerializer(serializers.Serializer):
    job_id = serializers.IntegerField()
    resume_id = serializers.IntegerField()

