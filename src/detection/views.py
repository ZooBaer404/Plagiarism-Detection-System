from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template import loader 
from detection.models import Admin
from django.contrib import messages
from urllib import request
from django.contrib import messages
from django.utils.text import slugify
from uuid import uuid4
from django.core.files.storage import default_storage, FileSystemStorage
from detection.models import *
from detection.forms import *
from .core.UploadResearchDocument import UniversityUploadProcess, UniversityUploadProcessDocuments
from .core.ProcessResearchDocument import *
from .core.UploadCheckingDocument import InstructorUploadProcessCheckingDocuments
from .core.ProcessCheckingDocument import *
from django.views.generic.edit import FormView
import torch
from sentence_transformers import util

def get_user_type(user):
    """
    Determines the user's account type based on their linked model.

    Checks the provided user instance across all role models (Admin, University, Instructor)
    and returns a string representing the user type.

    Args:
        user (User): The user instance to check.

    Returns:
        str: One of ["admin", "university", "instructor", "unknown"] depending on the match.

    Notes:
        - If the user is not found in any of the related role models, returns "unknown".
        - Helps route authenticated users to the correct dashboard.
    """

    try:
        admin = Admin.objects.get(user=user)
        return "admin"
    except Admin.DoesNotExist:
        pass

    try:
        university = University.objects.get(user=user)
        return "university"
    except University.DoesNotExist:
        pass

    try:
        instructor = Instructor.objects.get(user=user)
        return "instructor"
    except Instructor.DoesNotExist:
        pass

    return "unknown"  # If user is not found in any of the roles

def dashboard(request):
    """
    Redirects authenticated users to their respective dashboard based on session type.

    Determines the logged-in user's session type and redirects them accordingly:
        - Admin → admin_dashboard
        - University → university_dashboard
        - Instructor → instructor_dashboard

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse:
            - Redirects to the appropriate dashboard if authenticated.
            - Renders 'index.html' for unauthenticated users.

    Notes:
        - Uses 'type' stored in the session to determine user role.
        - Default fallback is the homepage if no session type is found.
    """

    user_type = request.session.get("type")
        
    if user_type == "admin":
        return redirect("admin_dashboard")
    elif user_type == "instructor":
        return redirect("instructor_dashboard")
    elif user_type == "university":
        return redirect("university_dashboard")

    return render(request, "index.html")

# ----------------------------------------
# LOGIN PAGE (UNIFIED)
# ----------------------------------------
def login_page(request):
    """
    Handles unified login for Admin, University, and Instructor users.

    This shared authentication view verifies credentials against each user type
    and redirects to their respective dashboard upon success.

    Args:
        request (HttpRequest): The incoming HTTP request containing POST data.

    Returns:
        HttpResponse:
            - Redirects to the appropriate dashboard upon successful authentication.
            - Renders 'login.html' with an error message if authentication fails.

    Notes:
        - Checks three models in order: Admin → University → Instructor.
        - Stores session keys ('type' and user ID) for role identification.
        - Displays an error message if credentials are invalid.
    """

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Check Admin
        admin = Admin.objects.filter(username=username, password=password).first()
        if admin:
            request.session["type"] = "admin"
            request.session["user_id"] = admin.id
            return redirect("admin_dashboard")

        # Check University
        uni = University.objects.filter(university_name=username, password=password).first()
        if uni:
            request.session["type"] = "university"
            request.session["university_id"] = uni.id
            return redirect("university_dashboard")

        # Check Instructor
        inst = Instructor.objects.filter(email=username, password=password).first()
        if inst:
            request.session["type"] = "instructor"
            request.session["instructor_id"] = inst.id
            return redirect("instructor_dashboard")

        # If nothing matched
        messages.error(request, "Invalid username or password")

    return render(request, "login.html")


# ----------------------------------------
# HELP PAGE
# ----------------------------------------
def help_page(request):
    """
    Displays the help and support page.

    Provides general guidance, FAQs, or support contact information for all user types.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders 'help.html'.
    """

    return render(request, "help.html")

def view_document(request, id):
    """
    Displays a single research document file for preview.

    Retrieves a specific document from the database and renders it in a viewer template.

    Args:
        request (HttpRequest): The incoming HTTP request.
        id (int): The ID of the ResearchDocument to view.

    Returns:
        HttpResponse: Renders 'view_document.html' with the document file context.

    Notes:
        - Used for in-browser PDF/document viewing.
        - Assumes the document exists; no error handling for missing IDs.
    """

    file = ResearchDocument.objects.get(id=id).research_document_file

    return render(request, "view_document.html", {
        "file": file
    })

def signup_page(request):
    """
    Displays the unified signup options page.

    Serves as an entry point for users to choose between
    Admin, University, or Instructor signup paths.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders 'signup.html'.
    """

    return render(request, "signup.html")

def continue_page(request):
    """
    Displays the continue page (intermediate navigation screen).

    Typically used to direct users to their next step in the authentication
    or onboarding process.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders 'continue.html'.
    """

    return render(request, "continue.html")