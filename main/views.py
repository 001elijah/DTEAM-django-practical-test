import json
import random
import re

from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from openai import OpenAI
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from CVProject.constants import AUDIT_BASE_URL, LOGS_BASE_URL, SETTINGS_BASE_URL

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
from .tasks import send_candidate_pdf_email
from .utils import generate_candidate_pdf

client = OpenAI(api_key=settings.OPENAI_API_KEY)


@login_required
def settings_page(request):
    context = {
        "tab_title": "Settings",
        "title": "Settings data",
        "home_btn_title": "< Home",
        "audit_logs_url": f"/{AUDIT_BASE_URL}{LOGS_BASE_URL}",
    }
    return render(request, "main/settings.html", context)


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
        "settings_url": f"/{SETTINGS_BASE_URL}",
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


def _get_languages():
    default_languages = [
        "Cornish",
        "Manx",
        "Breton",
        "Inuktitut",
        "Kalaallisut",
        "Romani",
        "Occitan",
        "Ladino",
        "Northern Sami",
        "Upper Sorbian",
        "Kashubian",
        "Zazaki",
        "Chuvash",
        "Livonian",
        "Tsakonian",
        "Saramaccan",
        "Bislama",
    ]
    languages = settings.TRANSLATING_LANGUAGES
    return languages.split(",") if languages else default_languages


def extract_clean_json(text: str):
    text = text.strip()
    text = text.replace('"```json"', "```json").replace('"```"', "```")

    match = re.search(r"```json\s*(.*?)\s*```", text, re.DOTALL)

    if match:
        json_str = match.group(1)
    else:
        json_str = text

    json_str = re.sub(r",\s*([\]}])", r"\1", json_str)

    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        print("JSON decode error:", e)
        print("Raw string was:\n", json_str)
        return None


def cv_content_to_translate(cv_detail_context):
    cv_content = {
        "no_bio_message": cv_detail_context.get(
            "no_bio_message", "No bio message is unavailable."
        ),
        "no_skills_message": cv_detail_context.get(
            "no_skills_message", "No skills message is unavailable."
        ),
        "no_projects_message": cv_detail_context.get(
            "no_projects_message", "No projects message is unavailable."
        ),
        "no_contacts_message": cv_detail_context.get(
            "no_contacts_message", "No contacts message is unavailable."
        ),
        "download_btn_title": cv_detail_context.get(
            "download_btn_title", "Download as PDF"
        ),
        "email_submit_btn_title": cv_detail_context.get(
            "email_submit_btn_title", "Send PDF to Email"
        ),
        "translate_btn_title": cv_detail_context.get(
            "translate_btn_title", "Translate"
        ),
        "skills_title": cv_detail_context.get("skills_title", "Skills"),
        "projects_title": cv_detail_context.get("projects_title", "Projects"),
        "contacts_title": cv_detail_context.get("contacts_title", "Contacts"),
        "bio_title": cv_detail_context.get("bio_title", "Bio"),
        "bio": cv_detail_context.get("bio", "No bio information available."),
        "projects": [],
    }

    context_projects = cv_detail_context.get("projects", [])
    for project_context in context_projects:
        cv_content["projects"].append(
            {
                "project_name": project_context.project_name,
                "project_description": project_context.project_description,
            }
        )

    return cv_content


def translate_cv_content(request, target_language, cv_detail_context):
    if not target_language:
        return render(request, "main/cv_detail.html", cv_detail_context)

    content_to_translate = json.dumps(
        cv_content_to_translate(cv_detail_context), indent=2, ensure_ascii=False
    )

    try:
        prompt = (
            f"You are a professional translator.\n"
            f"Translate the following JSON to {target_language}.\n"
            f"Return only valid JSON without comments or extra text.\n\n"
            f"{content_to_translate}"
        )

        response = client.responses.create(
            model="gpt-4o",
            instructions="You are a professional translator.",
            input=prompt,
            temperature=0.3,
        )

        translation = response.output_text

    except Exception as e:
        return JsonResponse({"Exception error": str(e)}, status=500)

    return translation


def _get_cv_detail_ui_context(candidate):
    languages_list = _get_languages()
    return {
        "languages_list": languages_list,
        "tab_title": f"{candidate.first_name} {candidate.last_name} CV",
        "home_btn_title": "< Home",
        "audit_logs_url": f"/{AUDIT_BASE_URL}{LOGS_BASE_URL}",
        "settings_url": f"/{SETTINGS_BASE_URL}",
        "download_btn_title": "Download as PDF",
        "email_submit_btn_title": "Send PDF to Email",
        "translate_btn_title": "Translate",
        "bio_title": "Bio",
        "skills_title": "Skills",
        "projects_title": "Projects",
        "contacts_title": "Contacts",
        "no_bio_message": "No bio information available.",
        "no_skills_message": "No skills information available.",
        "no_projects_message": "No projects information available.",
        "no_contacts_message": "No contacts information available.",
    }


@login_required
def cv_detail(request, pk):
    cv_detail_context = _get_cv_context(pk)
    candidate = cv_detail_context["candidate"]
    cv_detail_ui_context = _get_cv_detail_ui_context(candidate)

    cv_detail_context.update(cv_detail_ui_context)

    selected_language = request.GET.get("language")

    if selected_language:
        translation_data = translate_cv_content(
            request, selected_language, cv_detail_context
        )
        parsed_translation_data = extract_clean_json(translation_data)
        cv_detail_context.update(parsed_translation_data)

    return render(request, "main/cv_detail.html", cv_detail_context)


@login_required
def cv_generate_pdf(request, pk):
    return generate_candidate_pdf(pk)


@login_required
def send_cv_to_email(request, pk):
    if request.method == "POST":
        email = request.POST.get("email")
        if email:
            candidate = get_object_or_404(Candidate, pk=pk)
            send_candidate_pdf_email.delay(candidate.id, email)
            messages.success(
                request,
                f"PDF for {candidate.first_name} "
                f"{candidate.last_name} is being sent to "
                f"{email}.",
            )
        else:
            messages.error(request, "Please provide a valid email.")
    return redirect("cv_detail", pk=pk)


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
