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
import os
from django.core.files import File

def university_login(request):
    """
    Handles university authentication and session initialization.

    This view validates login credentials, ensures that the university
    is admin-approved, and initializes session variables for authorized access.

    Args:
        request (HttpRequest): The HTTP request containing form data and session info.

    Returns:
        HttpResponse:
            - Redirects to the university dashboard on successful login.
            - Renders 'login_university.html' or redirects with an error message on failure.

    Notes:
        - Prevents duplicate logins by clearing previous user sessions (admin/instructor).
        - Displays warnings if approval is pending.
    """

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
    """
    Displays the university account page.

    Verifies that the current session user is a university, then renders
    the university’s account information page.

    Args:
        request (HttpRequest): The current HTTP request with session data.

    Returns:
        HttpResponse: Renders 'university_account.html'.

    Notes:
        - Redirects unauthorized users to the dashboard with an error message.
        - Frontend-only page for account viewing.
    """

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
    Handles university signup with optional certificate upload.

    This view allows universities to register new accounts, optionally
    uploading an accreditation certificate. Submissions await admin approval.

    Args:
        request (HttpRequest): The incoming request containing form data and file uploads.

    Returns:
        HttpResponse:
            - Redirects to the login page on successful submission.
            - Renders 'signup_university.html' with validation errors on failure.

    Notes:
        - Uploaded certificates are stored safely using Django’s storage system.
        - Passwords are stored in plaintext (⚠️ should be hashed in production).
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
    """
    Registers a new university account.

    Handles the creation of a new university record with uploaded certificate.
    Requires all fields to be present.

    Args:
        request (HttpRequest): The HTTP request object containing POST and FILES data.

    Returns:
        HttpResponse:
            - Redirects to 'university_signup_done' after success.
            - Renders 'university_signup.html' on failure.
    """

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
    """
    Displays confirmation after successful university signup.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: Renders 'university_signup_done.html'.
    """

    return render(request, "university_signup_done.html")


def university_dashboard(request):
    """
    Displays the university dashboard with instructor and document management.

    This view:
    - Verifies university session authentication.
    - Shows lists of pending and approved instructors.
    - Displays uploaded research documents and any parsing errors.
    - Handles instructor approval and rejection actions.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        HttpResponse: Renders 'university_dashboard.html' with instructor and document data.

    Notes:
        - Access restricted to logged-in universities.
        - Processes POST requests for instructor approval or rejection.
    """

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
    """
    Approves, deletes, or manages instructors under a university.

    Verifies session authentication and processes instructor-related actions
    (approval or deletion) submitted through POST requests.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        HttpResponse: Renders 'university_instructors.html' with updated instructor lists.

    Notes:
        - Only available to university-type session users.
        - Displays success or warning messages depending on action.
    """

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
    """
    Handles research document uploads from universities.

    Displays the upload form, validates submissions, and saves documents
    for later parsing and plagiarism processing.

    Args:
        request (HttpRequest): The incoming HTTP request with file uploads.

    Returns:
        HttpResponse:
            - Redirects to 'university_upload_done' upon successful upload.
            - Renders 'university_upload.html' with validation messages on failure.

    Notes:
        - Only accessible to authenticated universities.
        - Uses Django form validation via ResearchDocumentUploadForm.
    """


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
    """
    Displays the upload confirmation and triggers document processing.

    After a successful upload, this view calls the
    `UniversityUploadProcessDocuments` function to analyze pending research papers.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: Renders 'university_upload_done.html' with pending papers list.

    Notes:
        - Access restricted to logged-in universities.
        - Displays success confirmation and processing summary.
    """


    university_id = request.session.get("university_id")
    if not university_id:
        messages.error(request, "Please login as university.")
        return redirect("university_login")

    university = University.objects.get(id=university_id)
    pending_research_papers = UniversityUploadProcessDocuments(university)

    return render(request, "university_upload_done.html", {"pending": pending_research_papers,})


def university_instructors(request):
    """
    Displays instructor management interface for universities.

    Args:
        request (HttpRequest): The current HTTP request.

    Returns:
        HttpResponse: Renders 'university_instructors.html'.

    Notes:
        - Frontend-only layout placeholder for instructor lists and management actions.
        - Restricted to authenticated university sessions.
    """

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
    """
    Lists research repositories uploaded by the university.

    Displays all documents uploaded by the university, allowing viewing or deletion.

    Args:
        request (HttpRequest): The HTTP request containing session and form data.

    Returns:
        HttpResponse: Renders 'university_repositories.html' with repository listings.

    Notes:
        - POST actions: 
            - 'view' renders individual repository.
            - 'delete' removes the document record.
    """

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
    """
    Displays a detailed view of a specific research document.

    Retrieves all associated text, vectors, statistics, images, references,
    and parsing errors for the selected document.

    Args:
        request (HttpRequest): The request object.
        id (int): The ID of the research document to display.

    Returns:
        HttpResponse: Renders 'university_repository.html' with document data.

    Notes:
        - Access restricted to the university that owns the document.
        - Displays NLP-parsed data, references, and error logs.
    """

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

    return render(request, "university_repository.html", {"document": research_document, 
                                                  "sentences": sentences, 
                                                  "vectors": vectors, 
                                                  "stats": stats,
                                                  "images": images,
                                                  "references": references,
                                                  "errors": errors,})

def university_repository_content(request, id):
    """
    Displays the content and parsed text of a research document.

    Provides sentence-level breakdown of the uploaded document along
    with a link to the original PDF for context.

    Args:
        request (HttpRequest): The request object.
        id (int): The research document ID.

    Returns:
        HttpResponse: Renders 'university_repository_content.html' with text and metadata.
    """

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

    research_document = ResearchDocument.objects.get(id=id)
    if not research_document:
        messages.error(request, "Research document not found!")
        redirect("dashboard")

    research_document_sentences = ResearchDocumentEnhancedText.objects.filter(research_document_id=research_document).order_by("created_at")
    research_document_pdf_url = research_document.research_document_file.url

    return render(request, "university_repository_content.html", {
        "document": research_document,
        "sentences": research_document_sentences,
        "pdf_url": research_document_pdf_url,
    })

def university_repository_content_sentence(request, id, sentence_id):
    """
    Highlights a specific sentence in a university research PDF.

    Opens the document, searches for the sentence, highlights it using
    PyMuPDF, and generates a temporary annotated PDF for display.

    Args:
        request (HttpRequest): The request object.
        id (int): The document ID.
        sentence_id (int): The sentence ID to highlight.

    Returns:
        HttpResponse: Renders 'university_repository_content_sentence.html' with the highlighted PDF.

    Notes:
        - Generates and saves a temporary highlighted copy in 'media/research/temp/'.
        - Useful for visual verification of text matches.
    """

    user_type = request.session.get("type")
    if user_type != "university" and user_type != "instructor":
        messages.error(request, "You are not logged in as a university or instructor")
        redirect("dashboard")
    
    
    if user_type == "university":
        university_id = request.session.get("university_id")
        if not university_id:
            messages.error(request, "Error: you are not authorized for this.")
            redirect("dashboard")
        
        university = University.objects.get(id=university_id)
        if not university:
            messages.error(request, "Error: you are not signed in as a university")
            redirect("dashboard")
    elif user_type == "instructor":
        instructor_id = request.session.get("instructor_id")
        if not instructor_id:
            messages.error(request, "Error: You are not authorized for this")
            redirect("dashboard")
        instructor = Instructor.objects.get(id=instructor_id)
        if not instructor:
            messages.error(request, "Error: you are not authorized for this")

    research_document = ResearchDocument.objects.get(id=id)
    research_document_sentences = ResearchDocumentEnhancedText.objects.filter(research_document_id=research_document).order_by("created_at")
    research_document_sentence = ResearchDocumentEnhancedText.objects.get(id=sentence_id)
    research_document_pdf_url = research_document.research_document_file.path

    doc = fitz.open(research_document_pdf_url)
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)

        text_instances = page.search_for(research_document_sentence.sentence_enhanced_text)

        for inst in text_instances:
            page.add_highlight_annot(inst)
    
    temp_path = f"media/research/temp/temp_{sentence_id}.pdf"
    os.makedirs(os.path.dirname(temp_path), exist_ok=True)
    doc.save(temp_path)
    doc.close()

    with open(temp_path, "rb") as f:
        temp_file = ResearchDocumentTempFile.objects.create(
            research_document_id=research_document,
        )
        temp_file.research_document.save(f"highlighted_{sentence_id}.pdf", File(f), save=True)

    research_document_pdf_url = temp_file.research_document.url

    return render(request, "university_repository_content_sentence.html", {
        "document": research_document,
        "sentences": research_document_sentences,
        "sentence_id": sentence_id,
        "pdf_url": research_document_pdf_url,
    })


def university_errors(request):
    """
    Displays parsing or upload errors for a university’s documents.

    Lists all research document errors associated with the logged-in university,
    including metadata and parsing failures.

    Args:
        request (HttpRequest): The HTTP request.

    Returns:
        HttpResponse: Renders 'university_errors.html' with error details.

    Notes:
        - Restricted to authenticated universities.
        - Useful for debugging failed or incomplete research uploads.
    """

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


