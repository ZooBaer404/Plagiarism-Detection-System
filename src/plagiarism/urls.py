"""
URL configuration for plagiarism project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import detection.views as default_views
import detection.instructor_views as instructor_views
import detection.university_views as university_views
import detection.admin_views as admin_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),

    # Public
    path("", default_views.dashboard, name="dashboard"),
    path("help/", default_views.help_page, name="help"),
    path("login/", default_views.login_page, name="login_page"),  # unified login (optional)
    # path("signup/", default_views.signup_page, name="signup_page"),
    path("continue/", default_views.continue_page, name="continue_page"),

    # Admin
    path("administrator/panel/", admin_views.admin_dashboard, name="admin_dashboard"),
    # path("administrator/login/", admin_views.login_admin, name="login_admin"),    
    path("administrator/", admin_views.admin_dashboard, name="admin_dashboard"),
    path("administrator/account/", admin_views.admin_account, name="admin_account"),
    path("administrator/universities/", admin_views.admin_universities, name="admin_universities"),
    path("administrator/pending/", admin_views.admin_pending, name="admin_pending"),
    path("administrator/reports/", admin_views.admin_reports, name="admin_reports"),
    path("administrator/activities/", admin_views.admin_activities, name="admin_activities"),

    # University
    path("university/signup/", university_views.university_signup, name="university_signup"),
    path("university/signup/done/", university_views.university_signup_done, name="university_signup_done"),
    path("university/login/", university_views.university_login, name="university_login"),
    path("university/approve_instructor/", university_views.university_approve_instructor, name="university_approve_instructor"),
    path("university/account/", university_views.university_account, name="university_account"),
    path("university/", university_views.university_dashboard, name="university_dashboard"),
    path("university/upload/", university_views.university_upload, name="university_upload"),
    path("university/upload/done/", university_views.university_upload_done, name="university_upload_done"),
    path("university/instructors/", university_views.university_approve_instructor, name="university_instructors"),
    path("university/pending/", university_views.university_approve_instructor, name="university_pending"),
    path("university/repositories/", university_views.university_repositories, name="university_repositories"),
    path("university/repositories/<int:id>", university_views.university_repository, name="university_repository"),
    path("university/repositories/repository/content/<int:id>", university_views.university_repository_content, name="university_repository_content"),
    path("university/content/<int:id>/<int:sentence_id>", university_views.university_repository_content_sentence, name="university_repository_content_sentence"),
    path("university/errors/", university_views.university_errors, name="university_errors"),

    # Instructor
    path("instructor/signup/", instructor_views.instructor_signup, name="instructor_signup"),
    path("instructor/signup/done/", instructor_views.instructor_signup_done, name="instructor_signup_done"),
    path("instructor/login/", instructor_views.instructor_login, name="instructor_login"),
    path("instructor/login/", instructor_views.instructor_login, name="login_instructor"),
    path("instructor/account/", instructor_views.instructor_account, name="instructor_account"),
    path("instructor/", instructor_views.instructor_dashboard, name="instructor_dashboard"),
    path("instructor/report/<int:id>", instructor_views.instructor_report, name="instructor_report"),
    path("instructor/checks/", instructor_views.instructor_checks, name="instructor_checks"),
    path("instructor/submissions/", instructor_views.instructor_submissions, name="instructor_submissions"),
    # path("instructor/repository/", instructor_views.instructor_repository, name="instructor_repository"),
    path("instructor/checks/<int:id>/references", instructor_views.instructor_report_references, name="instructor_report_reference"),
    path("instructor/checks/<int:id>/report/content", instructor_views.instructor_report_view_content, name="instructor_report_view_content"),
    path("instructor/checks/<int:id>/report/content/<int:sentence_id>", instructor_views.instructor_report_view_content_sentence, name="instructor_report_view_content_sentence"),
    path("instructor/checks/<int:id>", default_views.view_document, name="view_document"),
    path("instructor/checks/report/<int:checking_document_id>/content/differences", instructor_views.instructor_report_view_content_differences, name="instructor_report_view_content_difference_sentence"),
    # path("test", views.test_template, name="test_template"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)