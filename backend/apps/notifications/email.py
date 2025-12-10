from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from .models import DeliveryLog

class EmailService:
    @staticmethod
    def send_email(to_email, subject, template_name, context):
        """
        Renders an HTML template and sends it via Django's SMTP backend.
        """
        try:
            # 1. Render HTML
            # We assume templates are in 'templates/notifications/'
            html_content = render_to_string(f"notifications/{template_name}", context)
            
            # 2. Create Email Object
            email = EmailMultiAlternatives(
                subject=subject,
                body="Please view this email in an HTML-compatible viewer.", # Fallback text
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[to_email]
            )
            email.attach_alternative(html_content, "text/html")
            
            # 3. Send
            email.send()

            # 4. Log Success
            DeliveryLog.objects.create(
                recipient=to_email,
                channel=DeliveryLog.Channel.EMAIL,
                subject=subject,
                status="SENT"
            )
            return True

        except Exception as e:
            # 5. Log Failure
            DeliveryLog.objects.create(
                recipient=to_email,
                channel=DeliveryLog.Channel.EMAIL,
                subject=subject,
                status="FAILED",
                error_message=str(e)
            )
            return False