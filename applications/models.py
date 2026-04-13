from django.db import models
from django.conf import settings
from jobs.models import Job

class Application(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("shortlisted", "Shortlisted"),
        ("rejected", "Rejected"),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    candidate = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("job", "candidate")

    def __str__(self):
        return f"{self.candidate.username} - {self.job.title}"