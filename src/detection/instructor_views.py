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

def instructor_account(request):
    """
    Renders the Instructor Account page.

    Displays static instructor account information, such as profile details
    and basic navigation options. Does not modify any data.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the 'instructor_account.html' template.
    """

    return render(request, "instructor_account.html")

def instructor_dashboard(request):
    """
    Displays the main Instructor Dashboard and handles document uploads.

    This view allows instructors to:
    - Upload documents for plagiarism checking.
    - Process and compare documents against university research repositories.
    - View previous submissions and their corresponding plagiarism results.

    Args:
        request (HttpRequest): The incoming request object.

    Returns:
        HttpResponse: Renders the instructor dashboard with previous submissions.

    Notes:
        - Only accessible to logged-in instructors.
        - Uses sentence vector comparisons with cosine similarity for plagiarism detection.
        - Saves detailed plagiarism reports and results for each document.
    """


    instructor_id = request.session.get("instructor_id")
    if not instructor_id:
        messages.error(request, "Please login first.")
        return redirect("instructor_login")

    instructor = Instructor.objects.get(id=instructor_id)

    if request.method == "POST":
        document = request.FILES.get("document")
        if document:
            checking_document = CheckingDocument()
            checking_document.checking_document_name = document.name
            checking_document.checking_document_file = document
            checking_document.instructor_id = instructor
            checking_document.report_result = 0.0
            checking_document.save()

            sentence_vectors_obj = InstructorUploadProcessCheckingDocuments(instructor, checking_document)
            checking_document_info = CheckingDocumentBasicStats.objects.get(checking_document_id=checking_document)
            checking_document_no_sentences = checking_document_info.no_of_sentences

            percent_per_sentence = 100.0 / checking_document_no_sentences

            research_documents = ResearchDocument.objects.filter(university_id=checking_document.instructor_id.university_id)
            research_vectors = ResearchDocumentTextVector.objects.filter(research_document_id__in=research_documents)
            plagiarized_result = 0.0
            similarity_threshold = 0.85 # 85%

            print("there are ", len(sentence_vectors_obj), " many sentences to check")
            for checking_sentence in sentence_vectors_obj:
                check_tensor = torch.tensor(checking_sentence.text_vector).unsqueeze(0)
                
                if len(checking_sentence.checking_document_enhanced_text_id.sentence_enhanced_text) < 30: # if string length is less than this, skip it
                    continue

                for research_sentence in research_vectors:
                    research_tensor = torch.tensor(research_sentence.text_vector).unsqueeze(0)
                    similarity = util.cos_sim(check_tensor, research_tensor).item()

                    if similarity >= similarity_threshold:
                        CheckingDocumentCheckingProcess.objects.create(
                            checking_document_id=checking_document,
                            checking_document_text_vector_id=checking_sentence,
                            research_document_text_vector_id=research_sentence,
                            similarity=similarity
                        )

                        plagiarized_result += percent_per_sentence
                        print("plagiarized result has increased to ", plagiarized_result)

            checking_document_report_result = CheckingDocumentReport()
            checking_document_report_result.checking_document_id = checking_document
            checking_document_report_result.report_result = plagiarized_result
            checking_document_report_result.save()

            checking_document.report_result = plagiarized_result
            checking_document.save()

    previous_submissions = CheckingDocument.objects.filter(instructor_id=instructor)

    return render(request, "instructor_dashboard.html", {
        "previous_checks": previous_submissions,
    })


def instructor_signup(request: HttpRequest):
    """
    Handles instructor registration and validation.

    This view manages instructor sign-ups by:
    - Validating form inputs.
    - Ensuring the selected university exists.
    - Checking for duplicate accounts.
    - Creating a pending instructor record awaiting university approval.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        HttpResponse: 
            - Renders the signup page with validation messages on failure.
            - Redirects to the login page upon successful registration.

    Notes:
        - Uploaded certificates are saved with instructor details.
        - Passwords are stored in plaintext (⚠️ should be hashed in production).
    """

    # Retrieve all universities for dropdown selection
    universities = University.objects.all()
    form = InstructorForm()

    if request.method == "POST":
        # Extract and sanitize form inputs
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name")
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()
        certificate = request.FILES.get("certificate", "")
        field = request.POST.get("field", "").strip()
        university_id = request.POST.get("university_id", "").strip()

        # ------------------------------
        # 1️⃣ Basic Validation
        # ------------------------------
        if not all([first_name, last_name, email, password, certificate, field, university_id]):
            messages.error(request, "All fields are required.")
            return render(request, "instructor_signup.html", {"universities": universities})

        # ------------------------------
        # 2️⃣ Duplicate Check
        # ------------------------------
        if Instructor.objects.filter(email=email).exists():
            messages.error(request, "An instructor with this email already exists.")
            return render(request, "instructor_signup.html", {"universities": universities})

        # ------------------------------
        # 3️⃣ Validate University ID
        # ------------------------------
        try:
            uni = University.objects.get(pk=int(university_id))
        except (University.DoesNotExist, ValueError):
            messages.error(request, "Selected university is invalid.")
            return render(request, "instructor_signup.html", {"universities": universities})

        # ------------------------------
        # 4️⃣ Create Instructor Record
        # ------------------------------
        instructor = Instructor.objects.create(
            first_name=first_name,
            email=email,
            password=password,       # ⚠️ TODO: Hash password later
            university_id=uni,    # uses raw ID alias for FK field
            is_approved=False
        )
        
        # ------------------------------
        # 6️⃣ Success Feedback
        # ------------------------------
        messages.success(request, "Your signup has been submitted and is awaiting university approval.")
        return redirect("login_page")

    # ------------------------------
    # Render signup page (GET)
    # ------------------------------
    return render(request, "instructor_signup.html", {"universities": universities, "form": form, })


# ============================================================
#  VIEW: Instructor Signup Done
#  DESCRIPTION:
#     Displays a confirmation message after signup success.
# ============================================================
def instructor_signup_done(request):
    """
    Displays the confirmation page after a successful instructor sign-up.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: Renders the 'instructor_signup_done.html' template.
    """

    return render(request, "instructor_signup_done.html")


# ============================================================
#  VIEW: Instructor Login
#  DESCRIPTION:
#     Validates credentials and ensures the instructor is approved.
# ============================================================
def instructor_login(request):
    """
    Handles instructor authentication and session management.

    Validates the instructor’s credentials, checks approval status, and
    initializes session variables for authenticated access.

    Args:
        request (HttpRequest): The HTTP request containing login credentials.

    Returns:
        HttpResponse:
            - Redirects to the instructor dashboard upon successful login.
            - Renders the login form again on failure.

    Notes:
        - Displays warnings if the account is pending university approval.
        - Clears existing session data from other user roles before login.
    """


    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            # Attempt to find matching instructor
            inst = Instructor.objects.get(email=email, password=password)
            # approval = Instructor.objects.get(id=inst.id)

            # Check approval state
            if not inst.is_approved:
                messages.warning(request, "Your account is pending university approval.")
                return redirect("instructor_signup_done")

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

            # Store session and redirect
            request.session["type"] = "instructor"
            request.session["instructor_id"] = inst.id
            messages.success(request, "Login successful!")
            return redirect("instructor_dashboard")

        except Instructor.DoesNotExist:
            messages.error(request, "Invalid email or password.")

    # Render login form (GET)
    return render(request, "login_instructor.html")


# ============================================================
#  STATIC FRONTEND-ONLY PAGES (for prototype/demo)
# ============================================================

def instructor_report(request, id):
    """
    Displays a detailed plagiarism report for a specific document.

    This view retrieves all related data for a submitted document,
    including text, vectors, images, parsing errors, and plagiarism
    match results. It also compiles contextual text around matched
    segments for review.

    Args:
        request (HttpRequest): The HTTP request object.
        id (int): The ID of the checking document to display.

    Returns:
        HttpResponse: Renders 'instructor_report.html' with full report data.

    Notes:
        - Restricted to the document’s owner (instructor).
        - Displays pre- and post-context for each plagiarized segment.
    """

    user_type = request.session.get("type")
    if user_type != "instructor":
        messages.error(request, "You are not logged in as an instructor")
        redirect("dashboard")

    instructor_id = request.session.get("instructor_id")
    if not instructor_id:
        messages.error(request, "Error: you are not authorized for this report")
        redirect("instructor_dashboard")
    
    print("instructor id is ", instructor_id)

    instructor = Instructor.objects.get(id=instructor_id)
    if not instructor:
        messages.error(request, "Error: you are not signed in")
        redirect(request, "instructor_login")

    checking_document = CheckingDocument.objects.get(id=id)
    if not checking_document:
        messages.error(request, "Checking document not found!")
        redirect("instructor_dashboard")

    sentences = CheckingDocumentEnhancedText.objects.filter(checking_document_id=checking_document)
    vectors = CheckingDocumentTextVector.objects.filter(checking_document_id=checking_document)
    stats = CheckingDocumentBasicStats.objects.get(checking_document_id=checking_document)
    images = CheckingDocumentImages.objects.filter(checking_document_id=checking_document)
    errors = CheckingDocumentParseError.objects.filter(checking_document_id=checking_document)

    # research_references_before = list(list())
    # research_references_after = list(list())
    # research_references = list()

    checking_references_before = list(list())
    checking_references_after = list(list())
    checking_references = list()
    checking_process_references = CheckingDocumentCheckingProcess.objects.filter(checking_document_id=checking_document)
    for process in checking_process_references:
        checking_current_id = process.checking_document_text_vector_id.checking_document_enhanced_text_id.id
        # research_current_id = process.research_document_text_vector_id.research_document_enhanced_text_id.id

        checking_lower_bound_id = checking_current_id - 5
        # research_lower_bound_id = research_current_id - 5

        checking_upper_bound_id = checking_current_id + 5
        # research_upper_bound_id = research_current_id + 5

        checking_five_before = CheckingDocumentEnhancedText.objects.filter(id__lt=process.checking_document_text_vector_id.checking_document_enhanced_text_id.id, id__gte=checking_lower_bound_id)
        # research_five_before = ResearchDocumentEnhancedText.objects.filter(id__lt=process.research_document_text_vector_id.research_document_enhanced_text_id.id, id__gte=research_lower_bound_id)

        checking_five_after = CheckingDocumentEnhancedText.objects.filter(id__lte=checking_upper_bound_id, id__gt=process.checking_document_text_vector_id.checking_document_enhanced_text_id.id)
        # research_five_after = ResearchDocumentEnhancedText.objects.filter(id__lte=research_upper_bound_id, id__gt=process.research_document_text_vector_id.research_document_enhanced_text_id.id)

        checking_references.append(process.checking_document_text_vector_id.checking_document_enhanced_text_id)
        # research_references.append(process.research_document_text_vector_id.research_document_enhanced_text_id)

        checking_references_before.append(checking_five_before)
        # research_references_before.append(research_five_before)

        checking_references_after.append(checking_five_after)
        # research_references_after.append(research_five_after)

    checking_references_combined = zip(
        checking_references_before,
        checking_references,
        checking_references_after
    )

    # research_references_combined = zip(
    #     research_references_before,
    #     research_references,
    #     research_references_after
    # )

    # references_combined = zip(
    #     checking_references_combined,
    #     research_references_combined
    # )

    return render(request, "instructor_report.html", {"document": checking_document, 
                                                  "sentences": sentences, 
                                                  "vectors": vectors, 
                                                  "stats": stats,
                                                  "images": images,
                                                #   "references_combined": references_combined,
                                                  "checking_references_combined": checking_references_combined,
                                                #   "research_references_combined": research_references_combined,
                                                  "references": checking_process_references,
                                                  "errors": errors,})


def instructor_report_references(request, id):
    """
    Displays detailed reference comparison between checked and research documents.

    This report view shows the contextual relationship between the instructor’s
    document references and matching research paper references.

    Args:
        request (HttpRequest): The request object.
        id (int): The ID of the checking document to analyze.

    Returns:
        HttpResponse: Renders 'instructor_report_references.html' with paired reference data.

    Notes:
        - Shows sentences before and after each plagiarized match for both sides.
        - Useful for analyzing the accuracy of citation or reference overlaps.
    """

    user_type = request.session.get("type")
    if user_type != "instructor":
        messages.error(request, "You are not logged in as an instructor")
        redirect("dashboard")

    instructor_id = request.session.get("instructor_id")
    if not instructor_id:
        messages.error(request, "Error: you are not authorized for this report")
        redirect("instructor_dashboard")
    
    print("instructor id is ", instructor_id)

    instructor = Instructor.objects.get(id=instructor_id)
    if not instructor:
        messages.error(request, "Error: you are not signed in")
        redirect(request, "instructor_login")

    checking_document = CheckingDocument.objects.get(id=id)
    if not checking_document:
        messages.error(request, "Checking document not found!")
        redirect("instructor_dashboard")

    errors = CheckingDocumentParseError.objects.filter(checking_document_id=checking_document)

    research_references_before = list(list())
    research_references_after = list(list())
    research_references = list()

    checking_references_before = list(list())
    checking_references_after = list(list())
    checking_references = list()
    checking_process_references = CheckingDocumentCheckingProcess.objects.filter(checking_document_id=checking_document)
    for process in checking_process_references:
        checking_current_id = process.checking_document_text_vector_id.checking_document_enhanced_text_id.id
        research_current_id = process.research_document_text_vector_id.research_document_enhanced_text_id.id

        checking_lower_bound_id = checking_current_id - 5
        research_lower_bound_id = research_current_id - 5

        checking_upper_bound_id = checking_current_id + 5
        research_upper_bound_id = research_current_id + 5

        checking_five_before = CheckingDocumentEnhancedText.objects.filter(id__lt=process.checking_document_text_vector_id.checking_document_enhanced_text_id.id, id__gte=checking_lower_bound_id)
        research_five_before = ResearchDocumentEnhancedText.objects.filter(id__lt=process.research_document_text_vector_id.research_document_enhanced_text_id.id, id__gte=research_lower_bound_id)

        checking_five_after = CheckingDocumentEnhancedText.objects.filter(id__lte=checking_upper_bound_id, id__gt=process.checking_document_text_vector_id.checking_document_enhanced_text_id.id)
        research_five_after = ResearchDocumentEnhancedText.objects.filter(id__lte=research_upper_bound_id, id__gt=process.research_document_text_vector_id.research_document_enhanced_text_id.id)

        checking_references.append(process.checking_document_text_vector_id.checking_document_enhanced_text_id)
        research_references.append(process.research_document_text_vector_id.research_document_enhanced_text_id)

        checking_references_before.append(checking_five_before)
        research_references_before.append(research_five_before)

        checking_references_after.append(checking_five_after)
        research_references_after.append(research_five_after)

    checking_references_combined = zip(
        checking_references_before,
        checking_references,
        checking_references_after
    )

    research_references_combined = zip(
        research_references_before,
        research_references,
        research_references_after
    )

    paired_references = zip(
        checking_references_combined,
        research_references_combined
    )

    return render(request, "instructor_report_references.html", {"document": checking_document, 
                                                  "paired_references": paired_references,
                                                  "references": checking_process_references,})


def instructor_report_view_content(request, id):
    """
    Displays the full content of a submitted document, page by page.

    This view renders the extracted sentences and provides a preview link
    to the uploaded PDF document.

    Args:
        request (HttpRequest): The request object.
        id (int): The document ID.

    Returns:
        HttpResponse: Renders 'instructor_report_view_content.html' with document and sentence data.

    Notes:
        - Only accessible to the instructor who uploaded the document.
        - Fetches ordered sentence data and file URLs for inline preview.
    """

    user_type = request.session.get("type")
    if user_type != "instructor":
        messages.error(request, "You are not logged in as an instructor")
        redirect("dashboard")

    instructor_id = request.session.get("instructor_id")
    if not instructor_id:
        messages.error(request, "Error: you are not authorized for this report")
        redirect("instructor_dashboard")
    
    print("instructor id is ", instructor_id)

    instructor = Instructor.objects.get(id=instructor_id)
    if not instructor:
        messages.error(request, "Error: you are not signed in")
        redirect(request, "instructor_login")

    checking_document = CheckingDocument.objects.get(id=id)
    if not checking_document:
        messages.error(request, "Checking document not found!")
        redirect("instructor_dashboard")

    checking_document_sentences = CheckingDocumentEnhancedText.objects.filter(checking_document_id=checking_document).order_by("created_at")
    checking_document_pdf_url = checking_document.checking_document_file.url
    print("pdf url: ", checking_document.checking_document_file.url)

    return render(request, "instructor_report_view_content.html", {
        "document": checking_document,
        "sentences": checking_document_sentences,
        "pdf_url": checking_document_pdf_url,})


def instructor_report_view_content_sentence(request, id, sentence_id):
    """
    Highlights and previews a specific sentence within the uploaded PDF document.

    Opens the PDF using PyMuPDF, locates the target sentence, highlights it,
    and saves a temporary annotated copy for review.

    Args:
        request (HttpRequest): The request object.
        id (int): The ID of the checking document.
        sentence_id (int): The specific sentence ID to highlight.

    Returns:
        HttpResponse: Renders 'instructor_report_view_content_sentence.html' with the highlighted PDF.

    Notes:
        - Generates a temporary annotated file stored in 'media/checking/temp/'.
        - Helps instructors visually identify plagiarized or key text segments.
    """

    user_type = request.session.get("type")
    if user_type != "instructor":
        messages.error(request, "You are not logged in as an instructor")
        redirect("dashboard")

    instructor_id = request.session.get("instructor_id")
    if not instructor_id:
        messages.error(request, "Error: you are not authorized for this report")
        redirect("instructor_dashboard")
    
    print("instructor id is ", instructor_id)

    instructor = Instructor.objects.get(id=instructor_id)
    if not instructor:
        messages.error(request, "Error: you are not signed in")
        redirect(request, "instructor_login")

    checking_document = CheckingDocument.objects.get(id=id)
    if not checking_document:
        messages.error(request, "Checking document not found!")
        redirect("instructor_dashboard")

    checking_document_sentences = CheckingDocumentEnhancedText.objects.filter(checking_document_id=checking_document).order_by("created_at")
    checking_document_sentence = CheckingDocumentEnhancedText.objects.get(id=sentence_id)
    checking_document_pdf_url = checking_document.checking_document_file.path

    doc = fitz.open(checking_document_pdf_url)
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)

        text_instances = page.search_for(checking_document_sentence.sentence_enhanced_text)

        for inst in text_instances:
            page.add_highlight_annot(inst)
    
    temp_path = f"media/checking/temp/temp_{sentence_id}.pdf"
    os.makedirs(os.path.dirname(temp_path), exist_ok=True)
    doc.save(temp_path)
    doc.close()

    with open(temp_path, "rb") as f:
        temp_file = CheckingDocumentTempFile.objects.create(
            checking_document_id=checking_document,
        )
        temp_file.checking_document.save(f"highlighted_{sentence_id}.pdf", File(f), save=True)


    checking_document_pdf_url = temp_file.checking_document.url
    print("pdf url: ", checking_document.checking_document_file.url)

    return render(request, "instructor_report_view_content_sentence.html", {
        "document": checking_document,
        "sentences": checking_document_sentences,
        "sentence_id": sentence_id,
        "pdf_url": checking_document_pdf_url,})

def instructor_checks(request):
    """
    Lists all previous plagiarism checks performed by the instructor.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: Renders 'instructor_checks.html' with the list of checks.

    Notes:
        - Only accessible to logged-in instructors.
        - Each record links to its detailed plagiarism report.
    """

    user_type = request.session.get("type")
    if user_type != "instructor":
        messages.error(request, "You are not logged in as an instructor")
        redirect("dashboard")
    
    instructor_id = request.session.get("instructor_id")
    if not instructor_id:
        messages.error(request, "Error: you are not logged it")
        redirect("instructor_dashboard")

    instructor = Instructor.objects.get(id=instructor_id)
    checks_done_by_instructor = CheckingDocument.objects.filter(instructor_id=instructor)

    return render(request, "instructor_checks.html", {
        "checks": checks_done_by_instructor,
    })


def instructor_submissions(request):
    """
    Displays all submitted documents by the instructor.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders 'instructor_submissions.html'.

    Notes:
        - Static layout placeholder for future enhancements (e.g., filtering, sorting).
        - Access restricted to authenticated instructors.
    """

    user_type = request.session.get("type")
    if user_type != "instructor":
        messages.error(request, "You are not logged in as an instructor")
        redirect("dashboard")

    instructor_id = request.session.get("instructor_id")
    if not instructor_id:
        messages.error(request, "Error: you are not logged it")
        redirect("instructor_dashboard")

    instructor = Instructor.objects.get(id=instructor_id)

    return render(request, "instructor_submissions.html")


def instructor_repository(request):
    """
    Displays repositories uploaded by universities for instructor reference.

    Allows instructors to browse or access university-level research documents
    for comparison, learning, or future plagiarism checks.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: Renders 'instructor_repository.html'.

    Notes:
        - View is restricted to authenticated instructors.
        - Frontend-only placeholder for repository browsing features.
    """

    user_type = request.session.get("type")
    if user_type != "instructor":
        messages.error(request, "You are not logged in as an instructor")
        redirect("dashboard")
    
    instructor_id = request.session.get("instructor_id")
    if not instructor_id:
        messages.error(request, "Error: you are not logged it")
        redirect("instructor_dashboard")

    instructor = Instructor.objects.get(id=instructor_id)

    return render(request, "instructor_repository.html")
