from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage

from main.views.helpers import generate_candidate_pdf

from .models import Candidate


@shared_task
def send_candidate_pdf_email(candidate_id, email):
    candidate = Candidate.objects.get(id=candidate_id)
    pdf_response = generate_candidate_pdf(candidate.id)
    pdf_content = pdf_response.content

    subject = f"Candidate CV: {candidate.first_name} {candidate.last_name}"

    plain_message = (
        f"Dear User,\n\n"
        f"Please find attached the CV of {candidate.first_name} {candidate.last_name}."
    )

    email_message = EmailMessage(
        subject=subject,
        body=plain_message,
        from_email=settings.FROM_EMAIL,
        to=[email],
    )

    email_message.attach(
        f"{candidate.first_name}_{candidate.last_name}_CV.pdf",
        pdf_content,
        "application/pdf",
    )
    email_message.send()
