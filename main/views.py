import random

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from weasyprint import HTML

from .models import User


def cv_list(request):
    users = User.objects.all()
    return render(request, "main/cv_list.html", {"users": users})


def _get_cv_context(pk):
    user = get_object_or_404(User, pk=pk)

    skills = user.user_skills.select_related("skill")
    projects = user.user_projects.select_related("project")
    bio = user.bio.bio_item if hasattr(user, "bio") else None
    contacts = user.contacts.select_related("contact_type").all()

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
        "user": user,
        "skills": skills_with_random_classes,
        "projects": [up.project for up in projects],
        "bio": bio,
        "contacts": contacts,
    }


def cv_detail(request, pk):
    context = _get_cv_context(pk)
    return render(request, "main/cv_detail.html", context)


def cv_generate_pdf(request, pk):
    context = _get_cv_context(pk)

    html_content = render_to_string("main/cv_detail.html", context)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        f'inline; filename="{context["user"].first_name}_'
        f'{context["user"].last_name}_CV.pdf"'
    )
    HTML(string=html_content).write_pdf(response)

    return response
