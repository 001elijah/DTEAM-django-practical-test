import random

from django.shortcuts import get_object_or_404, render

from .models import User


def cv_list(request):
    users = User.objects.all()
    return render(request, "main/cv_list.html", {"users": users})


def cv_detail(request, pk):
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

    return render(
        request,
        "main/cv_detail.html",
        {
            "user": user,
            "skills": skills_with_random_classes,
            "projects": [up.project for up in projects],
            "bio": bio,
            "contacts": contacts,
        },
    )
