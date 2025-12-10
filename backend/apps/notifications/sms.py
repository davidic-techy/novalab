from django.conf import settings
from .models import DeliveryLog

# Optional: import twilio if installed
# from twilio.rest import Client 

class SMSService:
    @staticmethod
    def send_sms(phone_number, message):
        """
        Sends an SMS.
        """
        try:
            # --- REAL IMPLEMENTATION (Twilio Example) ---
            # client = Client(settings.TWILIO_SID, settings.TWILIO_TOKEN)
            # client.messages.create(body=message, from_=settings.TWILIO_NUMBER, to=phone_number)
            
            # --- MVP IMPLEMENTATION (Print to Console) ---
            print(f"==== SMS SENT TO {phone_number} ====")
            print(message)
            print("====================================")

            DeliveryLog.objects.create(
                recipient=phone_number,
                channel=DeliveryLog.Channel.SMS,
                status="SENT"
            )
            return True

        except Exception as e:
            DeliveryLog.objects.create(
                recipient=phone_number,
                channel=DeliveryLog.Channel.SMS,
                status="FAILED",
                error_message=str(e)
            )
            return False