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
    """
    Renders the Admin Pending page.

    This view validates that the current session user is an admin, ensuring proper authorization.
    If validation passes, it displays the 'admin_pending.html' page, typically showing pending
    university or instructor activities awaiting admin review.

    Args:
        request (HttpRequest): The HTTP request object containing session data.

    Returns:
        HttpResponse: Renders the 'admin_pending.html' template.

    Notes:
        - Redirects unauthorized users to the login page with an error message.
        - Relies on 'type' and 'user_id' stored in session for access control.
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

    return render(request, "admin_pending.html")


def admin_reports(request):
    """
    Displays all instructor and university reports for the admin panel.

    This view verifies admin access and retrieves all records from both
    `CheckingDocument` (instructor reports) and `ResearchDocument` (university reports),
    rendering them in the 'admin_reports.html' template.

    Args:
        request (HttpRequest): The HTTP request object containing session information.

    Returns:
        HttpResponse: Renders the reports page with both instructor and university reports.

    Notes:
        - Accessible only to authenticated admin users.
        - Shows combined insights from both report sources for administrative review.
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
    """
    Displays all recent activities in the admin dashboard.

    This view authenticates the admin user and aggregates recent actions
    and reports from both `CheckingDocument` (instructors) and `ResearchDocument` (universities).
    The data is then rendered in the 'admin_activities.html' page.

    Args:
        request (HttpRequest): The incoming request object.

    Returns:
        HttpResponse: Renders the admin activities overview page.

    Notes:
        - Restricted to logged-in admin users.
        - Combines instructor and university activities for unified visibility.
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

    university_reports = ResearchDocument.objects.all()
    reports = CheckingDocument.objects.all()

    return render(request, "admin_activities.html", {
        "reports": reports,
        "university_reports": university_reports,
    })

def login_admin(request):
    """
    Handles admin login authentication and session management.

    When accessed via POST, this view verifies the admin's username and password.
    Upon successful login, it stores the admin ID in the session and redirects to
    the admin dashboard. On GET, it simply renders the login page.

    Args:
        request (HttpRequest): The incoming request object.

    Returns:
        HttpResponse: 
            - Redirects to 'admin_dashboard' upon successful login.
            - Renders 'login_admin.html' for GET requests or failed authentication attempts.

    Notes:
        - Displays Django messages for login success or failure.
        - Session key used: 'admin' for storing admin ID.
    """


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
    """
    Displays the main admin dashboard with summarized platform statistics.

    This view authenticates the admin user and gathers:
    - Pending and approved universities.
    - Latest reports and activity logs from instructors and universities.
    - Aggregate statistics (total universities, instructors, and processed documents).

    Args:
        request (HttpRequest): The request object containing session and user data.

    Returns:
        HttpResponse: Renders the 'admin_dashboard.html' template with dashboard metrics.

    Notes:
        - Redirects unauthorized users to the login page.
        - Displays a summary of key metrics and recent activity logs for admins.
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
    Displays the Admin Account page (frontend only).

    This static view verifies that the user is an authenticated admin and
    renders account-related details along with a sign-out option.

    Args:
        request (HttpRequest): The request object containing session details.

    Returns:
        HttpResponse: Renders 'admin_account.html' template.

    Notes:
        - Primarily frontend display; does not modify account information.
        - Unauthorized users are redirected to the login page.
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
    Displays and manages the list of universities for the admin panel.

    This view shows all pending and approved universities and allows the admin
    to approve or reject universities directly via POST requests.

    Args:
        request (HttpRequest): The HTTP request object containing session and POST data.

    Returns:
        HttpResponse: Renders 'admin_universities.html' with pending and approved universities.

    Notes:
        - Accessible only to logged-in admin users.
        - Handles POST operations for approval/rejection.
        - Reflects updated university status immediately after admin action.
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



