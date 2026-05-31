from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_email(subject, to_email, template_name, context):
    html_content = render_to_string(template_name, context)

    email = EmailMultiAlternatives(
        subject=subject,
        body="",
        from_email=None,
        to=[to_email],
    )

    email.attach_alternative(html_content, "text/html")
    email.send()
