import io
import shutil
import tempfile
import fitz  # PyMuPDF
from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile

from detection.models import (
    University,
    Instructor,
    ResearchDocument,
    CheckingDocument,
    ResearchDocumentTempFile,
    CheckingDocumentTempFile,
)


# Temporary MEDIA_ROOT for test isolation
TEST_MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class ModelTests(TestCase):

    @classmethod
    def tearDownClass(cls):
        """Delete temporary media directory after all tests."""
        super().tearDownClass()
        shutil.rmtree(TEST_MEDIA_ROOT, ignore_errors=True)

    # -----------------------------------------------------------
    # Utility: create an in-memory PDF
    # -----------------------------------------------------------
    def create_pdf_file(self, text="Hello PDF"):
        buffer = io.BytesIO()
        doc = fitz.open()
        page = doc.new_page()
        page.insert_text((72, 72), text)
        doc.save(buffer)
        doc.close()
        buffer.seek(0)

        return SimpleUploadedFile("test.pdf", buffer.read(), content_type="application/pdf")

    # -----------------------------------------------------------
    # Create University
    # -----------------------------------------------------------
    def create_university(self):
        return University.objects.create(
            university_name="TestUniversity",
            email="uni@test.com",
            password="pass123",
            university_certificate=self.create_pdf_file("University Certificate")
        )

    # -----------------------------------------------------------
    # Create Instructor
    # -----------------------------------------------------------
    def create_instructor(self, university):
        return Instructor.objects.create(
            first_name="John",
            last_name="Doe",
            password="pass123",
            email="john@uni.com",
            university_id=university,
            certificate=self.create_pdf_file("Instructor Certificate"),
            field="Computer Science"
        )

    # -----------------------------------------------------------
    # TEST 1: University model
    # -----------------------------------------------------------
    def test_university_model(self):
        uni = self.create_university()

        self.assertEqual(uni.university_name, "TestUniversity")
        self.assertTrue(uni.university_certificate.name.startswith("certs/uni/uni_TestUniversity"))

    # -----------------------------------------------------------
    # TEST 2: Instructor model
    # -----------------------------------------------------------
    def test_instructor_model(self):
        uni = self.create_university()
        inst = self.create_instructor(uni)

        self.assertEqual(inst.university_id, uni)
        self.assertIn("inst_John_Doe", inst.certificate.name)

    # -----------------------------------------------------------
    # TEST 3: ResearchDocument model
    # -----------------------------------------------------------
    def test_research_document_model(self):
        uni = self.create_university()

        rd = ResearchDocument.objects.create(
            research_document_name="Research Paper 1",
            research_document_file=self.create_pdf_file("Research Content"),
            university_id=uni,
        )

        self.assertTrue(rd.research_document_file.name.startswith("research/university_TestUniversity"))
        self.assertFalse(rd.is_processed)
        self.assertTrue(rd.is_upload_complete)

    # -----------------------------------------------------------
    # TEST 4: CheckingDocument model
    # -----------------------------------------------------------
    def test_checking_document_model(self):
        uni = self.create_university()
        inst = self.create_instructor(uni)

        cd = CheckingDocument.objects.create(
            checking_document_name="CheckDoc1",
            checking_document_file=self.create_pdf_file("Checking Content"),
            instructor_id=inst
        )

        self.assertIn("checking/university_TestUniversity/ins_", cd.checking_document_file.name)
        self.assertIsNone(cd.report_result)

    # -----------------------------------------------------------
    # TEST 5: ResearchDocumentTempFile
    # -----------------------------------------------------------
    def test_research_document_temp_file(self):
        uni = self.create_university()

        rd = ResearchDocument.objects.create(
            research_document_name="Research Temp",
            research_document_file=self.create_pdf_file("abc"),
            university_id=uni,
        )

        temp = ResearchDocumentTempFile.objects.create(
            research_document_id=rd,
            research_document=self.create_pdf_file("Temp PDF")
        )

        self.assertIn("temp/", temp.research_document.name)

    # -----------------------------------------------------------
    # TEST 6: CheckingDocumentTempFile
    # -----------------------------------------------------------
    def test_checking_document_temp_file(self):
        uni = self.create_university()
        inst = self.create_instructor(uni)

        cd = CheckingDocument.objects.create(
            checking_document_name="CheckTemp",
            checking_document_file=self.create_pdf_file("xyz"),
            instructor_id=inst
        )

        temp = CheckingDocumentTempFile.objects.create(
            checking_document_id=cd,
            checking_document=self.create_pdf_file("Temp Checking")
        )

        self.assertIn("temp/", temp.checking_document.name)
