import random
from rest_framework_simplejwt.tokens import RefreshToken
from twilio.rest import Client

from CineSphere import settings


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    
def send_sms(user):
        otp = generate_otp()  
        phone_number = f"+{user.phone_number}"
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=f"Your authentication code is: {otp}",
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone_number
        )

        # Optionally, save the OTP in the database or session for verification later
        # user.otp = otp  # Assuming you've added an `otp` field to the User model
        # user.save()

        print(f"OTP sent to {phone_number}: {message.sid}")
        return otp 
    
def generate_otp():
    return str(random.randint(100000, 999999))  