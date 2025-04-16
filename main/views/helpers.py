import json
import random
import re

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from openai import OpenAI
from weasyprint import HTML

from CVProject.constants import AUDIT_BASE_URL, LOGS_BASE_URL, SETTINGS_BASE_URL
from main.models import Candidate

client = OpenAI(api_key=settings.OPENAI_API_KEY)


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


def _get_cv_detail_ui_context(candidate):
    languages_list = _get_languages()
    return {
        "languages_list": languages_list,
        "tab_title": f"{candidate.first_name} {candidate.last_name} CV",
        "home_btn_title": "< Home",
        "audit_logs_url": f"/{AUDIT_BASE_URL}{LOGS_BASE_URL}",
        "settings_url": f"/{SETTINGS_BASE_URL}",
        "download_btn_title": "Download PDF",
        "email_submit_btn_title": "Send PDF",
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
            "download_btn_title", "Download PDF"
        ),
        "email_submit_btn_title": cv_detail_context.get(
            "email_submit_btn_title", "Send PDF"
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


def translate_cv_content(target_language, cv_detail_context):
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
        print(f"Error translating CV content: {str(e)}")
        return JsonResponse({"Exception error": str(e)}, status=500)

    return translation


def process_cv_context(pk, selected_language=None):
    cv_detail_context = _get_cv_context(pk)
    candidate = cv_detail_context["candidate"]
    cv_detail_ui_context = _get_cv_detail_ui_context(candidate)
    cv_detail_context.update(cv_detail_ui_context)
    if selected_language:
        translation_data = translate_cv_content(selected_language, cv_detail_context)
        if isinstance(translation_data, JsonResponse):
            error_message = translation_data.status_code
            if error_message == 500:
                raise ValueError(
                    "An internal server error occurred. "
                    "Translation failed with status code 500."
                )
        if isinstance(translation_data, str):
            parsed_translation_data = extract_clean_json(translation_data)
            cv_detail_context.update(parsed_translation_data)

    return cv_detail_context


def generate_candidate_pdf(cv_detail_context):
    html_content = render_to_string("main/cv_detail.html", cv_detail_context)
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        f'inline; filename="{cv_detail_context["candidate"].first_name}_'
        f'{cv_detail_context["candidate"].last_name}_CV.pdf"'
    )
    HTML(string=html_content).write_pdf(response)
    return response


def remove_message(request):
    if request.method == "POST":
        data = json.loads(request.body)
        message_to_remove = data.get("message", "")

        storage = messages.get_messages(request)
        storage.used = False
        storage._queued_messages = [
            msg for msg in storage if str(msg) != message_to_remove
        ]

        return JsonResponse({"status": "success"})
