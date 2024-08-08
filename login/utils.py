import random
import requests
from django.core.cache import cache
from django.conf import settings
from TaqnyatSms import client
from .models import OtpMessage



def generate_otp():
    return random.randint(100000, 999999)

def send_otp(phone_number):
    otp = generate_otp()
    
    try:
        # Retrieve the OTP message template from the database
        template = OtpMessage.objects.get(name='otp_message_registeration')
        body = template.body.format(otp=otp)
        sender = 'OFAQ'
        scheduled = None  # Optional: Set this if you want to schedule the message

        taqnyt = client(settings.TAQNYAT_API_KEY)
        response = taqnyt.sendMsg(body, [phone_number], sender, scheduled)
        
        if response.get('status') == 'success':  # Adjust this based on actual response format
            cache.set(f'otp_{phone_number}', otp, timeout=300)  # Store OTP in cache for 5 minutes
            return True
        else:
            return False
    except OtpMessage.DoesNotExist:
        print("OTP message template not found")
        return False
    except Exception as e:
        print(f"Error sending OTP: {e}")
        return False

def verify_otp(phone_number, entered_otp):
    cached_otp = cache.get(f'otp_{phone_number}')
    if cached_otp and cached_otp == int(entered_otp):
        cache.delete(f'otp_{phone_number}')  # Remove OTP from cache after use
        return True
    return False
