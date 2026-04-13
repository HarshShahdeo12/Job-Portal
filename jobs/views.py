from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Job
from .forms import JobForm


def job_list(request):
    jobs = Job.objects.filter(is_active=True).order_by("-created_at")
    return render(request, "jobs/job_list.html", {"jobs": jobs})


@login_required
def post_job(request):
    if request.user.role != "recruiter":
        messages.error(request, "Only recruiters can post jobs.")
        return redirect("dashboard")

    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.recruiter = request.user
            job.save()
            messages.success(request, "Job posted successfully!")
            return redirect("my_jobs")
    else:
        form = JobForm()

    return render(request, "jobs/post_job.html", {"form": form})


@login_required
def my_jobs(request):
    if request.user.role != "recruiter":
        messages.error(request, "Only recruiters can view this page.")
        return redirect("dashboard")

    jobs = Job.objects.filter(recruiter=request.user).order_by("-created_at")
    return render(request, "jobs/my_jobs.html", {"jobs": jobs})