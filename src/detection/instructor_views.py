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


def instructor_account(request):
    return render(request, "instructor_account.html")

def instructor_dashboard(request):

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

            research_vectors = ResearchDocumentTextVector.objects.all()
            plagiarized_result = 0.0
            similarity_threshold = 0.85 # 85%

            print("there are ", len(sentence_vectors_obj), " many sentences to check")
            for checking_sentence in sentence_vectors_obj:
                check_tensor = torch.tensor(checking_sentence.text_vector).unsqueeze(0)
                
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
    return render(request, "instructor_signup_done.html")


# ============================================================
#  VIEW: Instructor Login
#  DESCRIPTION:
#     Validates credentials and ensures the instructor is approved.
# ============================================================
def instructor_login(request):

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
    Displays a static report preview for demonstration.
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


    checking_document_stats = CheckingDocumentBasicStats.objects.get(checking_document_id=checking_document)
    unique_content = 100 - checking_document.report_result
    matched_sources_ids = (
        CheckingDocumentCheckingProcess.objects
        .filter(checking_document_id=checking_document)
        .values_list("research_document_text_vector_id__research_document_id", flat=True)
        .distinct()
    )

    matched_sources_no = (
        CheckingDocumentCheckingProcess.objects
        .filter(checking_document_id=checking_document)
        .values("research_document_text_vector_id__research_document_id")
        .distinct()
        .count()
    )
    
    matched_sources = ResearchDocument.objects.filter(id__in=matched_sources_ids)

    checking_document_checking_process = CheckingDocumentCheckingProcess.objects.filter(checking_document_id=checking_document)

    return render(request, "instructor_report.html", {
        "checking_document": checking_document,
        "checking_document_report": checking_document.report_result,
        "checking_document_stats": checking_document_stats,
        "unique_content": unique_content,
        "matched_sources": matched_sources,
        "matched_sources_no": matched_sources_no,
        "checking_document_checking_process": checking_document_checking_process,
    })


def instructor_checks(request):
    """
    Lists previous plagiarism checks for the instructor.
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
    Displays all document submissions made by the instructor.
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
    Shows repositories uploaded by universities for reference.
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
