import logging

from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage

logger = logging.getLogger(__name__)


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
    try:
        email_message.send()
        logger.info(f"Email successfully sent to {email} for {first_name} {last_name}.")
        return "Email Sent Successfully"
    except Exception as e:
        logger.error(
            f"Failed to send email to {email} for {first_name} {last_name}: {str(e)}",
            exc_info=True,
        )
        raise
