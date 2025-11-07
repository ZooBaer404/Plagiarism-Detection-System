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

urlpatterns = [
    path("admin/", admin.site.urls),

    # Public
    path("", default_views.dashboard, name="dashboard"),
    path("help/", default_views.help_page, name="help"),
    path("login/", default_views.login_page, name="login_page"),  # unified login (optional)
    path("signup/", default_views.signup_page, name="signup_page"),
    path("continue/", default_views.continue_page, name="continue_page"),

    # Admin
    path("panel/admin/", admin_views.admin_dashboard, name="admin_dashboard"),
    path("login/admin/", admin_views.login_admin, name="login_admin"),
    path("dashboard/admin/", admin_views.admin_dashboard, name="admin_dashboard"),
    path("dashboard/admin/account/", admin_views.admin_account, name="admin_account"),
    path("dashboard/admin/universities/", admin_views.admin_universities, name="admin_universities"),
    path("dashboard/admin/pending/", admin_views.admin_pending, name="admin_pending"),
    path("dashboard/admin/reports/", admin_views.admin_reports, name="admin_reports"),
    path("dashboard/admin/activities/", admin_views.admin_activities, name="admin_activities"),

    # University
    path("signup/university/", university_views.university_signup, name="university_signup"),
    path("signup/university/done/", university_views.university_signup_done, name="university_signup_done"),
    path("login/university/", university_views.university_login, name="university_login"),
    path("university/approve_instructor/", university_views.university_approve_instructor, name="university_approve_instructor"),
    path("dashboard/university/account/", university_views.university_account, name="university_account"),
    path("dashboard/university/", university_views.university_dashboard, name="university_dashboard"),
    path("university/upload/", university_views.university_upload, name="university_upload"),
    path("university/upload/done/", university_views.university_upload_done, name="university_upload_done"),
    path("dashboard/university/instructors/", university_views.university_approve_instructor, name="university_instructors"),
    path("dashboard/university/pending/", university_views.university_approve_instructor, name="university_pending"),
    path("dashboard/university/repositories/", university_views.university_repositories, name="university_repositories"),
    path("dashboard/university/errors/", university_views.university_errors, name="university_errors"),

    # Instructor
    path("signup/instructor/", instructor_views.instructor_signup, name="instructor_signup"),
    path("signup/instructor/done/", instructor_views.instructor_signup_done, name="instructor_signup_done"),
    path("login/instructor/", instructor_views.instructor_login, name="instructor_login"),
    path("login/instructor/", instructor_views.instructor_login, name="login_instructor"),
    path("dashboard/instructor/account/", instructor_views.instructor_account, name="instructor_account"),
    path("dashboard/instructor/", instructor_views.instructor_dashboard, name="instructor_dashboard"),
    path("dashboard/instructor/report/<int:id>", instructor_views.instructor_report, name="instructor_report"),
    path("dashboard/instructor/checks/", instructor_views.instructor_checks, name="instructor_checks"),
    path("dashboard/instructor/submissions/", instructor_views.instructor_submissions, name="instructor_submissions"),
    path("dashboard/instructor/repository/", instructor_views.instructor_repository, name="instructor_repository"),
    path("document/<int:id>", default_views.view_document, name="view_document"),
    # path("test", views.test_template, name="test_template"),
]
