from django import forms
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import Admin, University, Instructor, ResearchDocument

class InstructorForm(forms.ModelForm):
    """
    Django ModelForm for creating or updating Instructor records.

    This form provides validated input fields for instructor registration,
    including personal information, university association, and certification upload.

    Meta:
        model (Instructor): The model linked to this form.
        fields (list): Defines which Instructor model fields are included in the form.
                       Includes:
                           - first_name
                           - last_name
                           - email
                           - password
                           - university_id
                           - certificate
                           - field
    """

    class Meta:
        model = Instructor
        fields = ["first_name", "last_name", "email", "password", "university_id", "certificate", "field"]

class UniversityApprovalForm(forms.Form):
    """
    Form for approving or rejecting universities by an admin.

    Provides a radio selection for admin users to mark a university’s
    approval status as either "Approve" or "Reject".

    Fields:
        is_approved (ChoiceField): Choice input rendered as radio buttons
                                   with two options — Approve or Reject.
    """

    choices = [("1", "Approve"), ("2", "Reject")]
    is_approved = forms.ChoiceField(widget=forms.RadioSelect, choices=choices)

class ResearchDocumentUploadForm(forms.ModelForm):
    """
    Django ModelForm for uploading research documents.

    Used by universities to submit research papers or reference documents.
    Automatically excludes university assignment and upload status fields
    as they are handled internally upon upload.

    Meta:
        model (ResearchDocument): The model linked to this form.
        fields (list): Includes only 'research_document_name' and 'research_document_file'.
        required (list): Both fields are mandatory for submission.
        exclude (list): Excludes 'university_id' and 'is_upload_complete' from user input.
    """

    class Meta:
        model = ResearchDocument
        fields = ["research_document_name", "research_document_file"]
        required = ["research_document_name", "research_document_file"]
        exclude = ["university_id", "is_upload_complete"]
