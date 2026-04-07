from django.urls import path
from . import views

urlpatterns = [
    path("jobs/", views.job_list, name="job_list"),
    path("jobs/post/", views.post_job, name="post_job"),
    path("jobs/my/", views.my_jobs, name="my_jobs"),
]