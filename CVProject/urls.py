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

from django.urls import path
from rest_framework.routers import DefaultRouter

from main import views
from main.views import UserViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")

urlpatterns = [
    path("", views.cv_list, name="cv_list"),
    path("cv/<int:pk>/", views.cv_detail, name="cv_detail"),
    path("cv/<int:pk>/download-pdf/", views.cv_generate_pdf, name="cv_generate_pdf"),
]

urlpatterns += router.urls
