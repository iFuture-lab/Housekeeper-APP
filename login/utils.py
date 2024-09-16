import random
import requests
from django.core.cache import cache
from django.conf import settings
from TaqnyatSms import client
from .models import OtpMessage,OTPLog
import json
import time
from django.utils import timezone
import logging
import random
import string

# Get an instance of a logger
logger = logging.getLogger(__name__)


################################## SMS API Integration ########################################################## 



def generate_otp():
    return random.randint(100000, 999999)

def send_otp(phone_number, force_resend=False,test_mode=False):
    # otp_key = f'otp_{phone_number}'
    # timestamp_key = f'otp_timestamp_{phone_number}'

    # # Check if OTP was sent less than 60 seconds ago
    # last_sent_time = cache.get(timestamp_key)
    # current_time = time.time()
    
    # if last_sent_time and (current_time - last_sent_time < 60) and not force_resend:
    #     return False, "Please wait before requesting a new OTP."
    
    
    last_sent = OTPLog.objects.filter(phone_number=phone_number).order_by('-created_at').first()
    current_time = timezone.now()
    
    if last_sent and (current_time - last_sent.created_at < timezone.timedelta(seconds=60)) and not force_resend:
        return False, "Please wait before requesting a new OTP."

    #otp = generate_otp()
    otp = '0000' if test_mode else generate_otp()
    
    try:
        if not test_mode:
            # body = f'Your OTP is {otp}'
            # Retrieve the OTP message template from the database
            template = OtpMessage.objects.get(name='otp_message')
            body = template.body.format(otp=otp)
            # template = OtpMessage.objects.filter(name='otp_message')
            # if template.exists():
            #     template = template.first()
            #     body = template.body.format(otp=otp)
            sender = 'OFAQ'
            scheduled = None  # Optional: Set this if you want to schedule the message
            taqnyt = client(settings.TAQNYAT_API_KEY)
            print([phone_number])
            response = taqnyt.sendMsg(body, [phone_number], sender, scheduled)
            print("Response:", response)  # For debugging
            response_data = json.loads(response)
            
            print(response_data)

            # Log the request and response
            x= OTPLog.objects.create(
                phone_number=phone_number,
                otp=otp,
                response_body=response
            )
            
            print(x)

            # if response_data.get('statusCode') == '201':
            #     return True, "OTP sent successfully."
            # else:
            #     return False, f"Failed to send OTP: {response_data}"
            return True, "OTP sent successfully."
        else:
            # Simulate success for test mode
            OTPLog.objects.create(
                phone_number=phone_number,
                otp=otp,
                
                
            )
            return True, "Test OTP sent successfully."
    except OtpMessage.DoesNotExist:
        return False, "OTP message template not found."
    # except json.JSONDecodeError:
    #     return False, "Failed to parse response."
    # except Exception as e:
    #     return False, f"Error sending OTP: {e}"
            
    
    #         response = taqnyt.sendMsg(body, [phone_number], sender, scheduled)  # save this to databse 
    #         response_data = json.loads(response)
    #         if response_data.get('status') == 'success':  # Adjust this based on actual response format
    #             cache.set(otp_key, otp, timeout=300)  # Store OTP in cache for 5 minutes
    #             cache.set(timestamp_key, current_time, timeout=300)  # Store the time OTP was sent
    #             return True, "OTP sent successfully."
    #         else:
    #             return False, f"Failed to send OTP: {response_data}"
    #     else:
    #         # Simulate success for test mode
    #         cache.set(otp_key, otp, timeout=300)  # Store OTP in cache for 5 minutes
    #         cache.set(timestamp_key, current_time, timeout=300)  # Store the time OTP was sent
    #         return True, "Test OTP sent successfully."
    # except OtpMessage.DoesNotExist:
    #     return False, "OTP message template not found."
    # except json.JSONDecodeError:
    #     return False, "Failed to parse response."
    # except Exception as e:
    #     return False, f"Error sending OTP: {e}"
        
       
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
    if cached_otp:
        if cached_otp == entered_otp:
            # Remove OTP from cache after successful use
            cache.delete(otp_key)
            cache.delete(f'otp_timestamp_{phone_number}')
            return True
    
    # Check the OTP in the database if not found or invalid in cache
    try:
        otp_record = OTPLog.objects.filter(
            phone_number=phone_number,
            otp=entered_otp,
            is_used=False
        ).order_by('-created_at').first()
        
        if otp_record:
            # Check if the OTP is within the valid time window (e.g., 1 minutes)
            expiration_time = timezone.now() - timezone.timedelta(minutes=1)
            if otp_record.created_at > expiration_time:
                # Mark OTP as used
                otp_record.is_used = True
                otp_record.save()
                
                # Optionally, you can cache the valid OTP for future quick checks
                cache.set(otp_key, entered_otp, timeout=300)  # Cache for 5 minutes
                return True
        
        return False
    except Exception as e:
        # Handle exceptions (e.g., logging)
        logger.error(f"Error verifying OTP: {e}", exc_info=True)
        return False
    # otp_key = f'otp_{phone_number}'
    # cached_otp = cache.get(otp_key)
    
    # # Handle OTP verification based on the mode
    # if test_mode:
    #     if entered_otp == '0000':  # Default OTP for testing
    #         cache.delete(otp_key)  # Remove OTP from cache after use
    #         cache.delete(f'otp_timestamp_{phone_number}')  # Remove timestamp from cache
    #         return True
    #     return False
    
    # # Production code
    # if cached_otp and cached_otp == entered_otp:
    #     cache.delete(otp_key)  # Remove OTP from cache after use
    #     cache.delete(f'otp_timestamp_{phone_number}')  # Remove timestamp from cache
    #     return True
    
    # return False


def resend_otp(phone_number,test_mode=False):
    return send_otp(phone_number, force_resend=True,test_mode=test_mode)



def generate_password_reset_token(length=6):
    """Generate a secure random password reset token."""
    characters = string.digits  # Typically, a token contains digits
    return ''.join(random.choice(characters) for _ in range(length))




def send_password_reset_token(phone_number, force_resend=False, test_mode=False):
   
    token = '123456' if test_mode else generate_password_reset_token()

    try:
        if not test_mode:
            # Retrieve the password reset message template from the database
            template = OtpMessage.objects.get(name='password_reset_message')
            body = template.body.format(otp=token)
            sender = 'OFAQ'
            scheduled = None  # Optional: Set this if you want to schedule the message
            taqnyt = client(settings.TAQNYAT_API_KEY)
            response = taqnyt.sendMsg(body, [phone_number], sender, scheduled)
            print("Response:", response)  # For debugging
            response_data = json.loads(response)
            
            OTPLog.objects.create(
                phone_number=phone_number,
                otp=token,
                response_body=response,
                created_at=timezone.now()
            )

            if response_data.get('status') == 'success':
                return True, "Password reset token sent successfully."
            else:
                return False, f"Failed to send password reset token: {response_data}"
        else:
            # Simulate success for test mode and log the OTP
            OTPLog.objects.create(
                phone_number=phone_number,
                otp=token,
                created_at=timezone.now()
            )
            return True, "Test password reset token sent successfully."
    except OtpMessage.DoesNotExist:
        return False, "Password reset message template not found."
    
    
    
def verify_password_reset_token(phone_number, entered_token,test_mode=False):
   
    if test_mode:
        # Check if the entered token matches the test token '123456'
        if entered_token == '123456':
            return True,"token verifed"
        else:
            return False, "Test mode: Invalid token."

    # Proceed with the normal token verification logic if not in test mode
    try:
        latest_log = OTPLog.objects.filter(phone_number=phone_number).order_by('-created_at').first()
        if not latest_log:
            return False, "No OTP found for this phone number."

        if latest_log.otp == entered_token:
            time_diff = timezone.now() - latest_log.created_at
            if time_diff.total_seconds() > 600:  # Token valid for 10 minutes (600 seconds)
                return False, "Token expired."
            return True, "Token verified successfully."
        else:
            return False, "Invalid token."
    except OTPLog.DoesNotExist:
        return False, "No OTP found for this phone number."
            

