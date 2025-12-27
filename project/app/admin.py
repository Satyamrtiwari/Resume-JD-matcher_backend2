from django.contrib import admin
from .models import JobDescription, Resume, MatchResult

# Register your models here.
admin.site.register(JobDescription)
admin.site.register(Resume)
admin.site.register(MatchResult)