from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["full_name", "phone", "skills", "resume",
                  "profile_pic", "experience", "education", "linkedin"]