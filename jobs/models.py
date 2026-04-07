from django.db import models
from django.conf import settings

class Job(models.Model):
    JOB_TYPE_CHOICES = [
        ("internship", "Internship"),
        ("full_time", "Full Time"),
        ("part_time", "Part Time"),
    ]

    recruiter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    location = models.CharField(max_length=120)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default="full_time")
    salary = models.IntegerField(null=True, blank=True)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.company_name}"
