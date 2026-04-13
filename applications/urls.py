from django.urls import path
from . import views

urlpatterns = [
    path("apply/<int:job_id>/", views.apply_job, name="apply_job"),

    path("recruiter/job/<int:job_id>/applicants/", views.applicants_for_job, name="applicants_for_job"),
    path("recruiter/application/<int:app_id>/<str:status>/", views.update_application_status, name="update_application_status"),
    path("my-applications/", views.my_applications, name="my_applications"),
]