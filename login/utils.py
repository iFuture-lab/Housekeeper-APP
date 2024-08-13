import random
import requests
from django.core.cache import cache
from django.conf import settings
from TaqnyatSms import client
from .models import OtpMessage
import json
import time



def generate_otp():
    return random.randint(100000, 999999)

def send_otp(phone_number, force_resend=False,test_mode=False):
    otp_key = f'otp_{phone_number}'
    timestamp_key = f'otp_timestamp_{phone_number}'

    # Check if OTP was sent less than 60 seconds ago
    last_sent_time = cache.get(timestamp_key)
    current_time = time.time()
    
    if last_sent_time and (current_time - last_sent_time < 60) and not force_resend:
        return False, "Please wait before requesting a new OTP."

    #otp = generate_otp()
    otp = '111111' if test_mode else generate_otp()
    
    try:
        if not test_mode:
            # Retrieve the OTP message template from the database
            template = OtpMessage.objects.get(name='otp_message_registeration')
            body = template.body.format(otp=otp)
            sender = 'OFAQ'
            scheduled = None  # Optional: Set this if you want to schedule the message
            taqnyt = client(settings.TAQNYAT_API_KEY)
            response = taqnyt.sendMsg(body, [phone_number], sender, scheduled)
            response_data = json.loads(response)
            if response_data.get('status') == 'success':  # Adjust this based on actual response format
                cache.set(otp_key, otp, timeout=300)  # Store OTP in cache for 5 minutes
                cache.set(timestamp_key, current_time, timeout=300)  # Store the time OTP was sent
                return True, "OTP sent successfully."
            else:
                return False, f"Failed to send OTP: {response_data}"
        else:
            # Simulate success for test mode
            cache.set(otp_key, otp, timeout=300)  # Store OTP in cache for 5 minutes
            cache.set(timestamp_key, current_time, timeout=300)  # Store the time OTP was sent
            return True, "Test OTP sent successfully."
    except OtpMessage.DoesNotExist:
        return False, "OTP message template not found."
    except json.JSONDecodeError:
        return False, "Failed to parse response."
    except Exception as e:
        return False, f"Error sending OTP: {e}"
        
       
def verify_otp(phone_number, entered_otp, test_mode=False):
    otp_key = f'otp_{phone_number}'
    cached_otp = cache.get(otp_key)
    
    # Handle OTP verification based on the mode
    if test_mode:
        if entered_otp == '0000':  # Default OTP for testing
            cache.delete(otp_key)  # Remove OTP from cache after use
            cache.delete(f'otp_timestamp_{phone_number}')  # Remove timestamp from cache
            return True
        return False
    
    # Production code
    if cached_otp and cached_otp == entered_otp:
        cache.delete(otp_key)  # Remove OTP from cache after use
        cache.delete(f'otp_timestamp_{phone_number}')  # Remove timestamp from cache
        return True
    
    return False


def resend_otp(phone_number,test_mode=False):
    return send_otp(phone_number, force_resend=True,test_mode=test_mode)
