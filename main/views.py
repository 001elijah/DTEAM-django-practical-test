import random

from django import forms
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from weasyprint import HTML

from CVProject.constants import AUDIT_BASE_URL, LOGS_BASE_URL

from .models import (
    BioItem,
    Candidate,
    CandidateProject,
    CandidateSkill,
    Contact,
    ContactType,
    Project,
    Skill,
)
from .serializers import (
    BioItemSerializer,
    CandidateProjectSerializer,
    CandidateSerializer,
    CandidateSkillSerializer,
    CandidateSummarySerializer,
    ContactSerializer,
    ContactTypeSerializer,
    ProjectSerializer,
    SkillSerializer,
    UserRegistrationSerializer,
)


@login_required
def cv_list(request):
    candidates = Candidate.objects.all()
    context = {
        "tab_title": "CV List",
        "title": "CV List",
        "hint": "Select a candidate to view their CV.",
        "no_candidates_message": "No candidates information available.",
        "candidates": candidates,
        "audit_logs_url": f"/{AUDIT_BASE_URL}{LOGS_BASE_URL}",
    }
    return render(request, "main/cv_list.html", context)


def _get_cv_context(pk):
    candidate = get_object_or_404(Candidate, pk=pk)

    skills = candidate.candidate_skills.select_related("skill")
    projects = candidate.candidate_projects.select_related("project")
    bio = candidate.bio.bio_item if hasattr(candidate, "bio") else None
    contacts = candidate.contacts.select_related("contact_type").all()

    skill_classes = [
        "bg-primary",
        "bg-success",
        "bg-danger",
        "bg-warning",
        "bg-info",
        "bg-dark",
    ]

    skills_with_random_classes = [
        {"skill_name": us.skill.skill_name, "class": random.choice(skill_classes)}
        for us in skills
    ]

    return {
        "candidate": candidate,
        "skills": skills_with_random_classes,
        "projects": [up.project for up in projects],
        "bio": bio,
        "contacts": contacts,
    }


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control-plaintext"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control-plaintext"})
    )


@login_required
def cv_detail(request, pk):
    context = _get_cv_context(pk)
    candidate_first_name = context["candidate"].first_name
    candidate_last_name = context["candidate"].last_name
    additional_context = {
        "tab_title": f"{candidate_first_name} {candidate_last_name} CV",
        "home_btn_title": "< Home",
        "audit_logs_url": f"/{AUDIT_BASE_URL}{LOGS_BASE_URL}",
        "download_btn_title": "Download as PDF",
        "bio_title": "Bio",
        "skills_title": "Skills",
        "projects_title": "Projects",
        "contacts_title": "Contacts",
        "no_bio_message": "No bio information available.",
        "no_skills_message": "No skills information available.",
        "no_projects_message": "No projects information available.",
        "no_contacts_message": "No contacts information available.",
    }
    context.update(additional_context)
    return render(request, "main/cv_detail.html", context)


@login_required
def cv_generate_pdf(request, pk):
    context = _get_cv_context(pk)

    html_content = render_to_string("main/cv_detail.html", context)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        f'inline; filename="{context["candidate"].first_name}_'
        f'{context["candidate"].last_name}_CV.pdf"'
    )

    HTML(string=html_content).write_pdf(response)

    return response


class UserRegistrationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully!"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    permission_classes = [IsAuthenticated]


class CandidateSummaryViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSummarySerializer
    http_method_names = ["get"]
    permission_classes = [IsAuthenticated]


class BioItemViewSet(viewsets.ModelViewSet):
    queryset = BioItem.objects.all()
    serializer_class = BioItemSerializer
    permission_classes = [IsAuthenticated]


class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticated]


class CandidateSkillViewSet(viewsets.ModelViewSet):
    queryset = CandidateSkill.objects.all()
    serializer_class = CandidateSkillSerializer
    http_method_names = ["get", "post", "delete"]
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        candidate_skill = self.get_object()
        skill = candidate_skill.skill

        candidate_skill.delete()

        if not CandidateSkill.objects.filter(skill=skill).exists():
            skill.delete()

        return Response(
            {"detail": "CandidateSkill and orphaned Skill (if any) deleted."},
            status=status.HTTP_204_NO_CONTENT,
        )


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]


class CandidateProjectViewSet(viewsets.ModelViewSet):
    queryset = CandidateProject.objects.all()
    serializer_class = CandidateProjectSerializer
    http_method_names = ["get", "post", "delete"]
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        candidate_project = self.get_object()
        project = candidate_project.project

        candidate_project.delete()

        if not CandidateProject.objects.filter(project=project).exists():
            project.delete()

        return Response(
            {"detail": "CandidateProject and orphaned Project (if any) deleted."},
            status=status.HTTP_204_NO_CONTENT,
        )


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]


class ContactTypeViewSet(viewsets.ModelViewSet):
    queryset = ContactType.objects.all()
    serializer_class = ContactTypeSerializer
    permission_classes = [IsAuthenticated]
