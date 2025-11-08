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



def university_login(request):
    if request.method == "POST":
        name = request.POST.get("university_name")
        password = request.POST.get("password")

        try:
            # Validate credentials
            university = University.objects.get(university_name=name, password=password)
        except University.DoesNotExist:
            messages.error(request, "Invalid university name or password.")
            return redirect("university_login")

        # Check admin approval
        approved = University.objects.filter(id=university.id, is_approved=True)
        if not approved:
            messages.warning(request, "Your account is pending admin approval.")
            return redirect("university_login")

        is_logged_in = request.session["type"]
        if is_logged_in:
            if is_logged_in == "instructor":
                del request.session["instructor_id"]
                del request.session["type"]
            elif is_logged_in == "university":
                del request.session["university_id"]
                del request.session["type"]
            elif is_logged_in == "amin":
                del request.session["admin_id"]
                del request.session["type"]    

        # Save session and redirect
        request.session["type"] = "university"
        request.session["university_id"] = university.id
        messages.success(request, f"Welcome, {university.university_name}!")
        return redirect("university_dashboard")

    # Render login page (GET)
    return render(request, "login_university.html")


def university_account(request):
    user_type = request.session.get("type")
    if user_type != "university":
        messages.error(request, "You are not logged in as a university")
        redirect("dashboard")
    
    university_id = request.session.get("university_id")
    if not university_id:
        messages.error(request, "Error: you are not authorized for this.")
        redirect("dashboard")
    
    university = University.objects.get(id=university_id)
    if not university:
        messages.error(request, "Error: you are not signed in as a university")
        redirect("dashboard")

    return render(request, "university_account.html")

# ----------------------------------------
# UNIVERSITY SIGNUP PAGE
# ----------------------------------------
def signup_university(request):
    """
    University signup — with certificate upload.
    """
    if request.method == "POST":
        uni_name = request.POST.get("university_name", "").strip()
        password = request.POST.get("password", "").strip()
        certificate = request.FILES.get("certificate")

        if not uni_name or not password:
            messages.error(request, "University name and password are required.")
            return render(request, "signup_university.html")

        cert_path = ""
        if certificate:
            safe_name = f"{slugify(uni_name)}_{uuid4().hex}_{certificate.name}"
            cert_path = default_storage.save(f"certs/universities/{safe_name}", certificate)

        University.objects.create(
            university_name=uni_name,
            password=password,
            university_certificate=cert_path or "",
        )

        messages.success(request, "Your registration has been submitted for approval.")
        return redirect("login_page")

    return render(request, "signup_university.html")

def university_signup(request):
    if request.method == "POST":
        name = request.POST.get("university_name")
        password = request.POST.get("password")
        certificate = request.FILES.get("university_certificate")

        # 1️⃣ Validation – all fields required
        if not name or not password or not certificate:
            messages.error(request, "All fields are required.")
            return redirect("university_signup")

        # 2️⃣ Save University record
        University.objects.create(
            university_name=name,
            password=password,  # ⚠️ TODO: Hash later
            university_certificate=certificate,
        )

        # 3️⃣ Redirect after success
        messages.success(request, "Your university has been registered successfully!")
        return redirect("university_signup_done")

    # Render signup form (GET)
    return render(request, "university_signup.html")

def university_signup_done(request):
    return render(request, "university_signup_done.html")


def university_dashboard(request):
    # --- Authentication guard ---
    
    user_type = request.session.get("type")
    if user_type != "university":
        messages.error(request, "You are not logged in as a university")
        redirect("dashboard")
    
    university_id = request.session.get("university_id")
    if not university_id:
        messages.error(request, "Error: you are not authorized for this.")
        redirect("dashboard")
    
    university = University.objects.filter(id=university_id).first()
    if not university:
        messages.error(request, "Error: you are not signed in as a university")
        redirect("dashboard")

    # --- Fetch instructors by status ---
    pending_instructors = Instructor.objects.filter(university_id=university, is_approved=False)
    approved_instructors = Instructor.objects.filter(university_id=university, is_approved=True)

    # --- Fetch Repositories ---
    documents = ResearchDocument.objects.filter(university_id=university)
    documents_errors = ResearchDocumentParseError.objects.filter(research_document_id__in=documents)

    # --- Handle Approve / Reject ---
    if request.method == "POST":
        approve_id = request.POST.get("approve_instructor")
        reject_id = request.POST.get("reject_instructor")

        # ✅ Approve Instructor
        if approve_id:
            try:
                instructor = Instructor.objects.get(id=approve_id)
                Instructor.objects.filter(
                    id=instructor.id, university_id=university
                ).update(is_approved=True)
                messages.success(request, f"{instructor.first_name} {instructor.last_name} approved")
            except Instructor.DoesNotExist:
                messages.error(request, "Instructor not found.")

        # ❌ Reject Instructor
        elif reject_id:
            try:
                instructor = Instructor.objects.get(id=reject_id)
                Instructor.objects.filter(
                    id=instructor, university_id=university
                ).update(is_approved=False)
                messages.warning(request, f"{instructor.first_name} {instructor.last_name} rejected")
            except Instructor.DoesNotExist:
                messages.error(request, "Instructor not found.")

        return redirect("university_dashboard")

    # --- Render dashboard ---
    return render(
        request,
        "university_dashboard.html",
        {
            "university": university,
            "pending_instructors": pending_instructors,
            "approved_instructors": approved_instructors,
            "documents": documents,
            "documents_errors": documents_errors,
        },
    )


def university_approve_instructor(request):
    user_type = request.session.get("type")
    if user_type != "university":
        messages.error(request, "You are not logged in as a university")
        redirect("dashboard")
    
    university_id = request.session.get("university_id")
    if not university_id:
        messages.error(request, "Error: you are not authorized for this.")
        redirect("dashboard")
    
    university = University.objects.get(id=university_id)
    if not university:
        messages.error(request, "Error: you are not signed in as a university")
        redirect("dashboard")

    university_instructors = Instructor.objects.filter(university_id=university)
    pending_university_approval = Instructor.objects.filter(university_id=university, is_approved=False)
    approved_university = Instructor.objects.filter(university_id=university, is_approved=True)

    # print("there are ", len(pending_university_approval), " pending instructors")
    # print("there are ", len(approved_university), " approved instructors")
    # print("typeof pending_university_approved ", pending_university_approval)

    if request.method == "POST":
        type = request.POST.get("type")

        # ✅ Approve
        if type == "approve":
            approve_id = request.POST.get("approve_instructor")
            instructor_approval = Instructor.objects.get(id=approve_id)
            instructor_approval.is_approved = True
            instructor_approval.save()

            messages.success(request, f"{instructor_approval.first_name} approved successfully!")

        ## ❌ Reject
        # elif type == "reject":
        #     reject_id = request.POST.get("reject_instructor")
        #     instructor_rejection = Instructor.objects.get(id=reject_id)
        #     instructor_rejection.is_approved = False
        #     instructor_rejection.message = "Rejected"
        #     instructor_rejection.save()

        #     messages.warning(request, f"{instructor_rejection.first_name} was rejected.")

        elif type == "delete":
            delete_id = request.POST.get("delete_instructor")
            instructor_deletion = Instructor.objects.get(id=delete_id)
            Instructor.delete(instructor_deletion)
            messages.warning(request, f"{instructor_deletion.first_name} was deleted.")

    # Render instructor list (instead of redirect)
    return render(request, "university_instructors.html", {
        "pending": pending_university_approval,
        "approved": approved_university,
        "universities": university_instructors,
    })


def university_upload(request):
    """Upload page for universities (frontend only)."""

    user_type = request.session.get("type")
    if user_type != "university":
        messages.error(request, "You are not logged in as a university")
        redirect("dashboard")
    
    university_id = request.session.get("university_id")
    if not university_id:
        messages.error(request, "Error: you are not authorized for this.")
        redirect("dashboard")
    
    university = University.objects.get(id=university_id)
    if not university:
        messages.error(request, "Error: you are not signed in as a university")
        redirect("dashboard")

    form = ResearchDocumentUploadForm()

    if request.method == "POST":
        form = ResearchDocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.university_id = university
            instance.is_upload_complete = True
            instance.save()

            return redirect("university_upload_done")
            
    return render(request, "university_upload.html", {"form": form})


def university_upload_done(request):
    """Upload confirmation page."""

    university_id = request.session.get("university_id")
    if not university_id:
        messages.error(request, "Please login as university.")
        return redirect("university_login")

    university = University.objects.get(id=university_id)
    pending_research_papers = UniversityUploadProcessDocuments(university)

    return render(request, "university_upload_done.html", {"pending": pending_research_papers,})


def university_instructors(request):
    """Instructor management page for universities."""
    user_type = request.session.get("type")
    if user_type != "university":
        messages.error(request, "You are not logged in as a university")
        redirect("dashboard")
    
    university_id = request.session.get("university_id")
    if not university_id:
        messages.error(request, "Error: you are not authorized for this.")
        redirect("dashboard")
    
    university = University.objects.get(id=university_id)
    if not university:
        messages.error(request, "Error: you are not signed in as a university")
        redirect("dashboard")

    return render(request, "university_instructors.html")


def university_repositories(request):
    """Repositories list uploaded by this university."""
    user_type = request.session.get("type")
    if user_type != "university":
        messages.error(request, "You are not logged in as a university")
        redirect("dashboard")
    
    university_id = request.session.get("university_id")
    if not university_id:
        messages.error(request, "Error: you are not authorized for this.")
        redirect("dashboard")
    
    university = University.objects.get(id=university_id)
    if not university:
        messages.error(request, "Error: you are not signed in as a university")
        redirect("dashboard")

    university_research_documents = ResearchDocument.objects.filter(university_id=university)

    if request.method == "POST":
        type = request.POST.get("type")
        paper_id = request.POST.get("paper_id")
        document = ResearchDocument.objects.get(id=paper_id)

        if type == "view":
            return render(request, "university_repository.html", {"repository": document})

        if type == "delete":
            ResearchDocument.delete(document)    

    return render(request, "university_repositories.html", {
        "repositories": university_research_documents,

    })

def university_repository(request, id):
    user_type = request.session.get("type")
    if user_type != "university":
        messages.error(request, "You are not authorized for this document")
        redirect("dashboard")

    university_id = request.session.get("university_id")
    print("university_id ", university_id)
    research_document = ResearchDocument.objects.get(id=id)

    if university_id != research_document.university_id.id:
        messages.error(request, "You are not authorized for this document")
        redirect("dashboard")

    sentences = ResearchDocumentEnhancedText.objects.filter(research_document_id=research_document)
    vectors = ResearchDocumentTextVector.objects.filter(research_document_id=research_document)
    stats = ResearchDocumentBasicStats.objects.get(research_document_id=research_document)
    images = ResearchDocumentImages.objects.filter(research_document_id=research_document)
    references = ResearchDocumentReferences.objects.filter(research_document_id=research_document)
    errors = ResearchDocumentParseError.objects.filter(research_document_id=research_document)

    return render(request, "view_document.html", {"document": research_document, 
                                                  "sentences": sentences, 
                                                  "vectors": vectors, 
                                                  "stats": stats,
                                                  "images": images,
                                                  "references": references,
                                                  "errors": errors,})


def university_errors(request):
    """Error logs: failed uploads, metadata issues, etc."""
    user_type = request.session.get("type")
    if user_type != "university":
        messages.error(request, "You are not logged in as a university")
        redirect("dashboard")
    
    university_id = request.session.get("university_id")
    if not university_id:
        messages.error(request, "Error: you are not authorized for this.")
        redirect("dashboard")
    
    university = University.objects.get(id=university_id)
    if not university:
        messages.error(request, "Error: you are not signed in as a university")
        redirect("dashboard")

    university_documents = ResearchDocument.objects.filter(university_id=university)
    errors = ResearchDocumentParseError.objects.filter(research_document_id__in=university_documents)

    return render(request, "university_errors.html", {"errors": errors,})


