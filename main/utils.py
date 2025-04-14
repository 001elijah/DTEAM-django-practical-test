from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML


def generate_candidate_pdf(candidate_id):
    # avoiding circular import by importing locally
    from main.views import _get_cv_context

    context = _get_cv_context(candidate_id)
    html_content = render_to_string("main/cv_detail.html", context)
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        f'inline; filename="{context["candidate"].first_name}_'
        f'{context["candidate"].last_name}_CV.pdf"'
    )
    HTML(string=html_content).write_pdf(response)
    return response
