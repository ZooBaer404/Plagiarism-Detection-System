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
    if request.user.is_authenticated:
        user_type = request.session.get("type")
        if user_type == "admin":
            redirect("admin_dashboard")
        elif user_type == "university":
            redirect("instructor_dashboard")
        elif user_type == "admin":
            redirect("university_dashboard")

    return render(request, "index.html")

# ----------------------------------------
# LOGIN PAGE (UNIFIED)
# ----------------------------------------
def login_page(request):
    """
    Shared login page for Admin, University, and Instructor.
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
    return render(request, "help.html")

def view_document(request, id):
    file = ResearchDocument.objects.get(id=id).research_document_file

    return render(request, "view_document.html", {
        "file": file
    })

def signup_page(request):
    return render(request, "signup.html")

def continue_page(request):
    return render(request, "continue.html")