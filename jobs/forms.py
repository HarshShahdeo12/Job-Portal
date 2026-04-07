from django import forms
from .models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ["title", "company_name", "location", "job_type", "salary", "description", "is_active"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. Software Developer Intern"}),
            "company_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. JP Morgan"}),
            "location": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. London / Remote"}),
            "job_type": forms.Select(attrs={"class": "form-select"}),
            "salary": forms.NumberInput(attrs={"class": "form-control", "placeholder": "e.g. 15000"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 6, "placeholder": "Write job responsibilities, requirements..."}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # checkbox class
        self.fields["is_active"].widget.attrs.update({"class": "form-check-input"})