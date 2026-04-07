from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from .models import Application
from jobs.models import Job


@login_required
def apply_job(request, job_id):
    if request.user.role != "candidate":
        messages.error(request, "Only candidates can apply.")
        return redirect("job_list")

    job = get_object_or_404(Job, id=job_id)

    if Application.objects.filter(job=job, candidate=request.user).exists():
        messages.error(request, "You already applied for this job.")
        return redirect("job_list")

   
    application = Application.objects.create(job=job, candidate=request.user)

    
    if job.recruiter and job.recruiter.email:
        send_mail(
            subject=f"New Application for {job.title}",
            message=(
                f"Hello {job.recruiter.username},\n\n"
                f"Candidate '{request.user.username}' has applied for your job '{job.title}'.\n"
                f"Login to your dashboard to review the application."
            ),
            from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
            recipient_list=[job.recruiter.email],
            fail_silently=True,
        )

    messages.success(request, "Applied successfully!")
    return redirect("job_list")


@login_required
def applicants_for_job(request, job_id):
    if request.user.role != "recruiter":
        messages.error(request, "Only recruiters can view applicants.")
        return redirect("dashboard")

    job = get_object_or_404(Job, id=job_id, recruiter=request.user)
    applications = Application.objects.filter(job=job).select_related("candidate").order_by("-applied_at")

    return render(request, "applications/applicants_for_job.html", {
        "job": job,
        "applications": applications
    })


@login_required
def update_application_status(request, app_id, status):
    if request.user.role != "recruiter":
        messages.error(request, "Only recruiters can update status.")
        return redirect("dashboard")

    application = get_object_or_404(Application, id=app_id)

    # Security check
    if application.job.recruiter != request.user:
        messages.error(request, "Not allowed.")
        return redirect("dashboard")

    if status not in ["pending", "shortlisted", "rejected"]:
        messages.error(request, "Invalid status.")
        return redirect("dashboard")

    application.status = status
    application.save()

   
    if status == "shortlisted" and application.candidate.email:
        send_mail(
            subject=f"Shortlisted for {application.job.title}",
            message=(
                f"Hello {application.candidate.username},\n\n"
                f"Congratulations! You have been shortlisted for the job '{application.job.title}'.\n"
                f"Please check your dashboard for further updates."
            ),
            from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
            recipient_list=[application.candidate.email],
            fail_silently=True,
        )

    messages.success(request, f"Status updated to {status}")
    return redirect("applicants_for_job", job_id=application.job.id)


@login_required
def my_applications(request):
    if request.user.role != "candidate":
        messages.error(request, "Only candidates can view this page.")
        return redirect("dashboard")

    apps = Application.objects.filter(candidate=request.user)\
        .select_related("job")\
        .order_by("-applied_at")

    return render(request, "applications/my_applications.html", {"apps": apps})