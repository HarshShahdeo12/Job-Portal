from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .models import Profile

def home(request):
    return render(request, "home.html")

def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = request.POST.get("role")  

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("signup")

        user = User.objects.create_user(username=username, email=email, password=password)
        user.role = role
        user.save()

        messages.success(request, "Account created! Please login.")
        return redirect("login")

    return render(request, "signup.html")

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is None:
            messages.error(request, "Invalid username or password")
            return redirect("login")

        login(request, user)
        return redirect("dashboard")

    return render(request, "login.html")

def user_logout(request):
    logout(request)
    return redirect("home")

@login_required
def dashboard(request):
    
    if request.user.role == "recruiter":
        return render(request, "recruiter_dashboard.html")
    return render(request, "candidate_dashboard.html")

@login_required
def edit_profile(request):
    if request.user.role != "candidate":
        messages.error(request, "Only candidates can edit profile.")
        return redirect("dashboard")

    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated!")
            return redirect("dashboard")
    else:
        form = ProfileForm(instance=profile)

    return render(request, "edit_profile.html", {"form": form})
