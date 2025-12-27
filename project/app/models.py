from django.db import models
#using django user
from django.contrib.auth.models import User


# Create your models here.


class JobDescription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=200)
    job_description = models.TextField()
    embedding = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)   

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    candidate_name = models.CharField(max_length=200)
    resume_file = models.FileField(upload_to='resumes/')
    text = models.TextField()
    embedding = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.candidate_name

class MatchResult(models.Model):
    job = models.ForeignKey(JobDescription, on_delete=models.CASCADE)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    
