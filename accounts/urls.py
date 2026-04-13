from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
]