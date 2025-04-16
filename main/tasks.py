from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage


@shared_task
def send_candidate_pdf_email(first_name, last_name, email, pdf_content):
    subject = f"Candidate CV: {first_name} {last_name}"

    plain_message = (
        f"Dear User,\n\n" f"Please find attached the CV of {first_name} {last_name}."
    )

    email_message = EmailMessage(
        subject=subject,
        body=plain_message,
        from_email=settings.FROM_EMAIL,
        to=[email],
    )

    email_message.attach(
        f"{first_name}_{last_name}_CV.pdf",
        pdf_content,
        "application/pdf",
    )
    email_message.send()
