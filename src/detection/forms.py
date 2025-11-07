from django import forms
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import Admin, University, Instructor, ResearchDocument

class InstructorForm(forms.ModelForm):
    class Meta:
        model = Instructor
        fields = ["first_name", "last_name", "email", "password", "university_id", "certificate", "field"]

class UniversityApprovalForm(forms.Form):
    choices = [("1", "Approve"), ("2", "Reject")]
    is_approved = forms.ChoiceField(widget=forms.RadioSelect, choices=choices)

class ResearchDocumentUploadForm(forms.ModelForm):
    class Meta:
        model = ResearchDocument
        fields = ["research_document_name", "research_document_file"]
        required = ["research_document_name", "research_document_file"]
        exclude = ["university_id", "is_upload_complete"]
