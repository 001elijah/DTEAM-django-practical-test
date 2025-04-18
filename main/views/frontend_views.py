from celery import current_app
from celery.result import AsyncResult
from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from CVProject.constants import AUDIT_BASE_URL, LOGS_BASE_URL, SETTINGS_BASE_URL
from main.models import Candidate
from main.tasks import send_candidate_pdf_email
from main.views.helpers import (
    _get_cv_context,
    _get_cv_detail_ui_context,
    generate_candidate_pdf,
    process_cv_context,
)


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control-plaintext"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control-plaintext"})
    )


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


@login_required
def cv_detail(request, pk):
    error_message = None  # Initialize error message
    selected_language = request.GET.get("language")

    try:
        cv_detail_context = process_cv_context(pk, selected_language)
    except Exception as e:
        error_message = f"Failed to load CV details: {str(e)}"
        cv_detail_context = _get_cv_context(pk)
        candidate = cv_detail_context["candidate"]
        cv_detail_ui_context = _get_cv_detail_ui_context(candidate)
        cv_detail_context.update(cv_detail_ui_context)

    cv_detail_context.update(
        {
            "error_message": error_message,
        }
    )

    return render(request, "main/cv_detail.html", cv_detail_context)


@login_required
def cv_generate_pdf(request, pk):
    selected_language = request.GET.get("language")
    cv_detail_context = process_cv_context(pk, selected_language)
    return generate_candidate_pdf(cv_detail_context)


@login_required
def send_cv_to_email(request, pk):
    if request.method == "POST":
        email = request.POST.get("email")
        selected_language = request.POST.get("language")
        if email:
            try:
                validate_email(email)
                cv_detail_context = process_cv_context(pk, selected_language)
                pdf_response = generate_candidate_pdf(cv_detail_context)
                pdf_content = pdf_response.content

                candidate = get_object_or_404(Candidate, pk=pk)
                task_id = send_candidate_pdf_email.delay(
                    candidate.first_name, candidate.last_name, email, pdf_content
                )

                try:
                    result = AsyncResult(task_id.id, app=current_app)
                    print(f"Task result => {result.get()}")
                    if result.failed():
                        raise Exception(f"Task failed with error: {result.result}")
                except Exception as e:
                    print(f"Error sending PDF to email: {str(e)}")
                    messages.error(
                        request,
                        f"Error: Failed to send the CV email to {email}. "
                        "Please try again.",
                    )

                messages.success(
                    request,
                    f"PDF for {candidate.first_name} "
                    f"{candidate.last_name} is being sent to "
                    f"{email}.",
                )
                if selected_language:
                    return redirect(
                        reverse("cv_detail", kwargs={"pk": pk})
                        + f"?language={selected_language}"
                    )
                else:
                    return redirect("cv_detail", pk=pk)

            except ValidationError:
                messages.error(request, "Please provide a valid email address.")

            except Exception as e:
                messages.error(request, f"Failed to send PDF: {str(e)}")
    return redirect("cv_detail", pk=pk)
