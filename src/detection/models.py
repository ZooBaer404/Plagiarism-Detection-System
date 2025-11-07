from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields.array import ArrayField
from django.core.validators import FileExtensionValidator

# Create your models here.

class Admin(models.Model):
    username = models.CharField(max_length=255, null=False)
    password = models.CharField(max_length=255, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified_at = models.DateTimeField(auto_now=True)
  
class University(models.Model):
    def certificate_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/certs/uni/uni_<name>/<filename>
        return "certs/uni/uni_{0}/{1}".format(instance.university_name, filename)
    
    university_name = models.CharField(max_length=255, null=False)
    email = models.EmailField(max_length=320, null=False, default="example@example.com")
    password = models.CharField(max_length=255, null=False)
    university_certificate = models.FileField(upload_to=certificate_directory_path, null=False)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified_at = models.DateTimeField(auto_now=True)

# class UniversityApproval(models.Model):
#     admin_id = models.ForeignKey(Admin, on_delete=models.CASCADE)
#     is_approved = models.BooleanField(default=False)
#     university_id = models.ForeignKey(University, on_delete=models.CASCADE, null=False)
#     message = models.TextField(max_length=1000, null=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     last_modified_at = models.DateTimeField(auto_now=True)

class UniversityLogin(models.Model):
    ip_address = models.CharField(max_length=16)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified_at = models.DateTimeField(auto_now=True)

class Instructor(models.Model):
    def certificate_directory_path(instance, filename):
        return "certs/inst/inst_{0}_{1}/{2}".format(instance.first_name, instance.last_name, filename)
    
    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=False)
    password = models.CharField(max_length=255, null=False)
    email = models.EmailField(max_length=320, unique=True, null=False)
    university_id = models.ForeignKey(University, on_delete=models.CASCADE, null=False)
    certificate = models.FileField(upload_to=certificate_directory_path, null=False)
    field = models.CharField(max_length=100, null=False)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified_at = models.DateTimeField(auto_now=True)
        
# class InstructorApproval(models.Model):
#     university_id = models.ForeignKey(University, on_delete=models.CASCADE)
#     is_approved = models.BooleanField(default=False)
#     instructor_id = models.ForeignKey(Instructor, on_delete=models.CASCADE, null=False)
#     message = models.TextField(max_length=1000, null=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     last_modified_at = models.DateTimeField(auto_now=True)
    
class InstructorLogin(models.Model):
    ip_address = models.CharField(max_length=16)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified_at = models.DateTimeField(auto_now=True)
    
class UniversityLogout(models.Model):
    university_id = models.ForeignKey(University, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified_at = models.DateTimeField(auto_now=True)
    
# class ResearchRepository(models.Model):
#     repo_name = models.CharField(max_length=255, null=False)
#     university_id = models.ForeignKey(University, on_delete=models.CASCADE, null=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     last_modified_at = models.DateTimeField(auto_now=True)
    
# class ResearchDocumentUpload(models.Model):
#     research_repository_id = models.ForeignKey(ResearchRepository, on_delete=models.CASCADE, null=False)
#     research_document_name = models.CharField(max_length=255, null=False)
#     reseach_document_path = models.CharField(max_length=1000, null=False)
#     is_upload_complete = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     last_modified_at = models.DateTimeField(auto_now=True)
    
class ResearchDocument(models.Model):
    def research_document_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/certs/uni/uni_<name>/<filename>
        return "research/university_{0}/{1}".format(instance.university_id.university_name, filename)
    
    research_document_name = models.CharField(max_length=500)
    # research_document_path = models.CharField(max_length=1000, null=False)
    research_document_file = models.FileField(upload_to=research_document_directory_path, null=False, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    university_id = models.ForeignKey(University, on_delete=models.CASCADE, null=False)
    # research_repository_id = models.ForeignKey(ResearchRepository, on_delete=models.CASCADE, null=False)
    # research_document_upload_id = models.ForeignKey(ResearchDocumentUpload, on_delete=models.CASCADE, null=False)
    is_upload_complete = models.BooleanField(default=True)
    is_processed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified_at = models.DateTimeField(auto_now=True)
    
# class ResearchDocumentUploadError(models.Model):
#     # research_document_upload_id = models.ForeignKey(ResearchDocumentUpload, on_delete=models.CASCADE, null=False)
#     research_document_id = models.ForeignKey(ResearchDocument, on_delete=models.CASCADE, null=False)
#     error_message = models.TextField(max_length=1000, null=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     last_modified_at = models.DateTimeField(auto_now=True)
    
class ResearchDocumentParseText(models.Model):
    # research_document_upload_id = models.ForeignKey(ResearchDocumentUpload, on_delete=models.CASCADE, null=False)
    research_document_id = models.ForeignKey(ResearchDocument, on_delete=models.CASCADE, null=False)
    parse_text = models.TextField(max_length=50000, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified_at = models.DateTimeField(auto_now=True)
    
class ResearchDocumentReferences(models.Model):
    research_document_id = models.ForeignKey(ResearchDocument, on_delete=models.CASCADE, null=False)
    index = models.IntegerField(default=-1, null=False)
    reference_text = models.CharField(max_length=50000, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified_at = models.DateTimeField(auto_now=True)
        
class ResearchDocumentParseError(models.Model):
    research_document_id = models.ForeignKey(ResearchDocument, on_delete=models.CASCADE, null=False)
    parse_text = models.TextField(max_length=50000, null=False)
    error_message = models.CharField(max_length=1000, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified_at = models.DateTimeField(auto_now=True)
        
# class ResearchDocumentSectionTokens(models.Model):
#     research_document = models.ForeignKey(ResearchDocument, on_delete=models.CASCADE, null=False)
#     section_index = models.IntegerField(null=False)
#     section_title = models.CharField(max_length=1000, null=False)
#     section_description = models.TextField(max_length=5000, null=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     last_modified_at = models.DateTimeField(auto_now=True)
        
class ResearchDocumentBasicStats(models.Model):
    research_document_id = models.ForeignKey(ResearchDocument, on_delete=models.CASCADE)
    no_of_references = models.IntegerField()
    no_of_sentences = models.IntegerField()
    no_of_characters = models.IntegerField()
    no_of_words = models.IntegerField()
    size_of_document = models.IntegerField()
    no_of_images = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified_at = models.DateTimeField(auto_now=True)
    
class ResearchDocumentImages(models.Model):
    def research_document_directory_image_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/certs/uni/uni_<name>/<filename>
        return "research/document_image_{0}/{1}".format(instance.research_document_id, filename)
    
    research_document_id = models.ForeignKey(ResearchDocument, on_delete=models.CASCADE)
    image = models.FileField(upload_to=research_document_directory_image_path, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified_at = models.DateTimeField(auto_now=True)
    
class ResearchDocumentEnhancedText(models.Model):
    research_document_id = models.ForeignKey(ResearchDocument, on_delete=models.CASCADE)
    sentence_index = models.IntegerField()
    sentence_enhanced_text = models.TextField(max_length=50000, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified_at = models.DateTimeField(auto_now=True)
    
class ResearchDocumentTextVector(models.Model):
    research_document_id = models.ForeignKey(ResearchDocument, on_delete=models.CASCADE)
    research_document_enhanced_text_id = models.ForeignKey(ResearchDocumentEnhancedText, on_delete=models.CASCADE)
    text_vector = ArrayField(base_field=models.FloatField())
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified_at = models.DateTimeField(auto_now=True)    

# class CheckingDocumentUpload(models.Model):
#     checking_document_name = models.CharField(max_length=500, null=False)
#     checking_document_path = models.CharField(max_length=1000, null=False)
#     is_upload_complete = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     last_modified_at = models.DateTimeField(auto_now=True)
    
class CheckingDocument(models.Model):
    def research_document_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/certs/uni/uni_<name>/<filename>
        return "checking/university_{0}/ins_{1}/{2}".format(instance.instructor_id.university_id.university_name, instance.instructor_id, filename)
    checking_document_name = models.CharField(max_length=500)
    # checking_document_path = models.CharField(max_length=1000, null=False)
    checking_document_file = models.FileField(upload_to=research_document_directory_path, null=False, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    instructor_id = models.ForeignKey(Instructor, on_delete=models.CASCADE, null=False)
    # checking_document_upload_id = models.ForeignKey(CheckingDocumentUpload, on_delete=models.CASCADE, null=False)
    report_result = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified_at = models.DateTimeField(auto_now=True)
        
class CheckingDocumentUploadError(models.Model):
    checking_document_id = models.ForeignKey(CheckingDocument, on_delete=models.CASCADE, null=False)
    error_message = models.TextField(max_length=1000, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified_at = models.DateTimeField(auto_now=True)
        
class CheckingDocumentImages(models.Model):
    def checking_document_directory_image_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/certs/uni/uni_<name>/<filename>
        return "checking/document_image_{0}/{1}".format(instance.checking_document_id, filename)
    
    checking_document_id = models.ForeignKey(CheckingDocument, on_delete=models.CASCADE)
    image = models.FileField(upload_to=checking_document_directory_image_path, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified_at = models.DateTimeField(auto_now=True)

class CheckingDocumentParseText(models.Model):
    checking_document_id = models.ForeignKey(CheckingDocument, on_delete=models.CASCADE, null=False)
    parse_text = models.TextField(max_length=50000, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified_at = models.DateTimeField(auto_now=True)
    
class CheckingDocumentReferences(models.Model):
    checking_document_id = models.ForeignKey(CheckingDocument, on_delete=models.CASCADE, null=False)
    index = models.IntegerField(default=-1)
    reference_text = models.CharField(max_length=50000, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified_at = models.DateTimeField(auto_now=True)
    
class CheckingDocumentParseError(models.Model):
    checking_document_id = models.ForeignKey(CheckingDocument, on_delete=models.CASCADE, null=False)
    parse_text = models.TextField(max_length=50000, null=False)
    error_message = models.CharField(max_length=1000, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified_at = models.DateTimeField(auto_now=True)
    
# class CheckingDocumentSectionTokens(models.Model):
#     checking_document_id = models.ForeignKey(CheckingDocument, on_delete=models.CASCADE, null=False)
#     section_index = models.IntegerField(null=False)
#     section_title = models.CharField(max_length=1000, null=False)
#     section_description = models.TextField(max_length=5000, null=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     last_modified_at = models.DateTimeField(auto_now=True)
        
class CheckingDocumentBasicStats(models.Model):
    checking_document_id = models.ForeignKey(CheckingDocument, on_delete=models.CASCADE, null=False)
    no_of_references = models.IntegerField()
    no_of_sentences = models.IntegerField()
    no_of_characters = models.IntegerField()
    no_of_words = models.IntegerField()
    size_of_document = models.IntegerField()
    no_of_images = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified_at = models.DateTimeField(auto_now=True)
    
# class CheckingDocumentImages(models.Model):
#     def checking_document_directory_image_path(instance, filename):
#         # file will be uploaded to MEDIA_ROOT/certs/uni/uni_<name>/<filename>
#         return "checking/document_image_{0}/{1}".format(instance.checking_document_id, filename)
    
#     checking_document_id = models.ForeignKey(CheckingDocument, on_delete=models.CASCADE)
#     image = models.FileField(upload_to=checking_document_directory_image_path, null=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     last_modified_at = models.DateTimeField(auto_now=True)

class CheckingDocumentEnhancedText(models.Model):
    checking_document_id = models.ForeignKey(CheckingDocument, on_delete=models.CASCADE)
    sentence_index = models.IntegerField()
    sentence_enhanced_text = models.CharField(max_length=50000, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified_at = models.DateTimeField(auto_now=True)
    
class CheckingDocumentTextVector(models.Model):
    checking_document_id = models.ForeignKey(CheckingDocument, on_delete=models.CASCADE, null=False)
    checking_document_enhanced_text_id = models.ForeignKey(CheckingDocumentEnhancedText, on_delete=models.CASCADE, null=False)
    text_vector = ArrayField(models.IntegerField())
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified_at = models.DateTimeField(auto_now=True)
    
class CheckingDocumentCheckingProcess(models.Model):
    checking_document_id = models.ForeignKey(CheckingDocument, on_delete=models.CASCADE, null=False)
    checking_document_text_vector_id = models.ForeignKey(CheckingDocumentTextVector, on_delete=models.CASCADE, null=False)
    research_document_text_vector_id = models.ForeignKey(ResearchDocumentTextVector, on_delete=models.CASCADE, null=False)
    similarity = models.FloatField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified_at = models.DateTimeField(auto_now=True)
    
class CheckingDocumentReport(models.Model):
    checking_document_id = models.ForeignKey(CheckingDocument, on_delete=models.CASCADE, null=False)
    report_result = models.FloatField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified_at = models.DateTimeField(auto_now=True)
