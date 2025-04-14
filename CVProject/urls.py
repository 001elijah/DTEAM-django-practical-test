"""
URL configuration for CVProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from django.contrib.auth import views as auth_views
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from CVProject.constants import (
    API_BASE_URL,
    API_URLS,
    AUDIT_BASE_URL,
    BASE_URL,
    SETTINGS_BASE_URL,
)
from main import views
from main.views import (
    BioItemViewSet,
    CandidateProjectViewSet,
    CandidateSkillViewSet,
    CandidateSummaryViewSet,
    CandidateViewSet,
    ContactTypeViewSet,
    ContactViewSet,
    ProjectViewSet,
    SkillViewSet,
    UserRegistrationView,
)

router = DefaultRouter()
router.register(
    API_URLS["candidates"].strip("/"), CandidateViewSet, basename="candidate"
)
router.register(API_URLS["bio_items"].strip("/"), BioItemViewSet, basename="bio_item")
router.register(API_URLS["skills"].strip("/"), SkillViewSet, basename="skill")
router.register(
    API_URLS["candidate_skills"].strip("/"),
    CandidateSkillViewSet,
    basename="candidate_skill",
)
router.register(API_URLS["projects"].strip("/"), ProjectViewSet, basename="project")
router.register(
    API_URLS["candidate_projects"].strip("/"),
    CandidateProjectViewSet,
    basename="candidate_project",
)
router.register(API_URLS["contacts"].strip("/"), ContactViewSet, basename="contact")
router.register(
    API_URLS["contact_types"].strip("/"), ContactTypeViewSet, basename="contact_type"
)
router.register(
    API_URLS["candidate_summaries"].strip("/"),
    CandidateSummaryViewSet,
    basename="candidate_summary",
)

# API routes
api_patterns = [
    path("register/", UserRegistrationView.as_view(), name="user_register"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

# Admin/Employer routes
admin_patterns = [
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(next_page="cv_list"),
        name="login",
    ),
    path(
        "accounts/logout/",
        auth_views.LogoutView.as_view(next_page="login"),
        name="logout",
    ),
    path("", views.cv_list, name="cv_list"),
    path("cv/<int:pk>/", views.cv_detail, name="cv_detail"),
    path("cv/<int:pk>/download-pdf/", views.cv_generate_pdf, name="cv_generate_pdf"),
    path(
        "cv/<int:pk>/send-pdf-email/", views.send_cv_to_email, name="send_cv_to_email"
    ),
]

urlpatterns = [
    path(API_BASE_URL.lstrip("/"), include(api_patterns)),
    path(BASE_URL, include(admin_patterns)),
    path(AUDIT_BASE_URL, include("audit.urls")),
    path(SETTINGS_BASE_URL, views.settings_page, name="settings_page"),
]

urlpatterns += router.urls
