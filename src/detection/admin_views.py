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
from detection.core.UploadResearchDocument import UniversityUploadProcess, UniversityUploadProcessDocuments
from detection.core.ProcessResearchDocument import *
from detection.core.UploadCheckingDocument import InstructorUploadProcessCheckingDocuments
from detection.core.ProcessCheckingDocument import *
from django.views.generic.edit import FormView
import torch
from sentence_transformers import util


def admin_pending(request):
    user_type = request.session.get("type")
    if user_type != "admin":
        messages.error(request, "You are not logged in as an Admin")
        redirect("login_page")
    
    admin_id = request.session.get("user_id")
    if not admin_id:
        messages.error(request, "Error: you are not authorized for this.")
        redirect("login_page")
    
    admin = Admin.objects.filter(id=admin_id).first()
    if not admin:
        messages.error(request, "Error: you are not signed in as a admin")
        redirect("login_page")

    return render(request, "admin_pending.html")


def admin_reports(request):
    """
    Displays the Latest Reports page (frontend only).
    """
    user_type = request.session.get("type")
    if user_type != "admin":
        messages.error(request, "You are not logged in as an Admin")
        redirect("login_page")
    
    admin_id = request.session.get("user_id")
    if not admin_id:
        messages.error(request, "Error: you are not authorized for this.")
        redirect("login_page")
    
    admin = Admin.objects.filter(id=admin_id).first()
    if not admin:
        messages.error(request, "Error: you are not signed in as a admin")
        redirect("login_page")

    reports = CheckingDocument.objects.all()
    university_reports = ResearchDocument.objects.all()

    return render(request, "admin_reports.html", {"reports": reports, "university_reports": university_reports,})


def admin_activities(request):
    user_type = request.session.get("type")
    if user_type != "admin":
        messages.error(request, "You are not logged in as an Admin")
        redirect("login_page")
    
    admin_id = request.session.get("user_id")
    if not admin_id:
        messages.error(request, "Error: you are not authorized for this.")
        redirect("login_page")
    
    admin = Admin.objects.filter(id=admin_id).first()
    if not admin:
        messages.error(request, "Error: you are not signed in as a admin")
        redirect("login_page")

    university_reports = ResearchDocument.objects.all()
    reports = CheckingDocument.objects.all()

    return render(request, "admin_activities.html", {
        "reports": reports,
        "university_reports": university_reports,
    })


# ----------------------------------------# ADMIN LOGIN PAGE
# ----------------------------------------

def login_admin(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        admin = Admin.objects.get(username=username, password=password)

        if admin:
            request.session["admin"] = admin.id
            messages.success(request, "Login successful!")
            return redirect("admin_dashboard")


    return render(request, "login_admin.html")



# ----------------------------------------
# DASHBOARDS
# ----------------------------------------

def admin_dashboard(request):
    user_type = request.session.get("type")
    if user_type != "admin":
        messages.error(request, "You are not logged in as an Admin")
        redirect("login_page")
    
    admin_id = request.session.get("user_id")
    if not admin_id:
        messages.error(request, "Error: you are not authorized for this.")
        redirect("login_page")
    
    admin = Admin.objects.filter(id=admin_id).first()
    if not admin:
        messages.error(request, "Error: you are not signed in as a admin")
        redirect("login_page")

    # ✅ get only universities that have NO approval yet
    # approved_uni_ids = University.objects.filter(is_approved=True)
    # all_uni_ids_with_records = University.objects.all()
    pending_unis = University.objects.filter(is_approved=False)
    approved_unis = University.objects.filter(is_approved=True)
    latest_reports = CheckingDocumentReport.objects.all().order_by("created_at")
    latest_instructor_activities = CheckingDocument.objects.all().order_by("created_at")
    latest_university_activities = ResearchDocument.objects.all().order_by("created_at")
    total_universities = University.objects.count()
    total_instructors = Instructor.objects.count()
    total_documents_processed = CheckingDocument.objects.count()

    print("there are", len(pending_unis), " pending universities")
    print("there are", len(approved_unis), " approved universities")


    # if request.method == "POST":
    #     approve_id = request.POST.get("approve_uni")
    #     reject_id = request.POST.get("reject_uni")
    #     admin_id = request.session.get("user_id")
    #     admin = Admin.objects.get(id=admin_id)

    #     if approve_id:
    #         uni = University.objects.get(id=approve_id)
    #         UniversityApproval.objects.update_or_create(
    #             university=uni,
    #             defaults={
    #                 "admin_id": admin,
    #                 "is_approved": True,
    #                 "message": f"{uni.university_name} approved",
    #             },
    #         )
    #         messages.success(request, f"{uni.university_name} approved successfully!")
    #         return redirect("admin_dashboard")

    #     if reject_id:
    #         uni = University.objects.get(id=reject_id)
    #         UniversityApproval.objects.update_or_create(
    #             university=uni,
    #             defaults={
    #                 "admin_id": admin,
    #                 "is_approved": False,
    #                 "message": f"{uni.university_name} rejected",
    #             },
    #         )
    #         messages.warning(request, f"{uni.university_name} rejected.")
    #         return redirect("admin_dashboard")

    return render(
        request,
        "admin_dashboard.html",
        {"pending_unis": pending_unis, "approved_unis": approved_unis, 
         "latest_reports": latest_reports, "latest_instructor_activities": latest_instructor_activities, 
         "latest_university_activities": latest_university_activities,
         "total_universities": total_universities,
         "total_instructors": total_instructors,
         "total_documents_processed": total_documents_processed,},
    )


def admin_account(request):
    """
    Frontend-only Admin Account page.
    Displays account info and sign out button (static layout).
    """
    user_type = request.session.get("type")
    if user_type != "admin":
        messages.error(request, "You are not logged in as an Admin")
        redirect("login_page")
    
    admin_id = request.session.get("user_id")
    if not admin_id:
        messages.error(request, "Error: you are not authorized for this.")
        redirect("login_page")
    
    admin = Admin.objects.filter(id=admin_id).first()
    if not admin:
        messages.error(request, "Error: you are not signed in as a admin")
        redirect("login_page")


    return render(request, "admin_account.html")



def admin_universities(request):
    """
    Frontend-only Admin Universities page.
    Displays pending, approved, and rejected universities (static layout).
    """

    user_type = request.session.get("type")
    if user_type != "admin":
        messages.error(request, "You are not logged in as an Admin")
        redirect("login_page")
    
    admin_id = request.session.get("user_id")
    if not admin_id:
        messages.error(request, "Error: you are not authorized for this.")
        redirect("login_page")
    
    admin = Admin.objects.filter(id=admin_id).first()
    if not admin:
        messages.error(request, "Error: you are not signed in as a admin")
        redirect("login_page")

    approved_unis_ids = University.objects.filter(is_approved=True)
    all_uni_ids_with_records = University.objects.all()
    pending_unis = University.objects.filter(is_approved=False)
    approved_unis = University.objects.filter(is_approved=True)

    if request.method == "POST":
        type = request.POST.get("type")
        university_id = request.POST.get("university_id")
        university = University.objects.get(id=university_id)

        if type == "approve":
            if university:
                university.is_approved = True
                university.save()
            else:
                messages.error(request, "University not found")
        elif type == "reject":
            if university:
                university.is_approved = False
                university.save()

    return render(request, "admin_universities.html",
                {"pending_unis": pending_unis,
                "approved_unis": approved_unis,
                })



