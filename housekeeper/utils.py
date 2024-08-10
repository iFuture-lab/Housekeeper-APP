# utils.py
from django.utils.timezone import now
from .models import ActionLog
from django.contrib.auth.models import AnonymousUser
from .models import CustomUser
import random
from django.core.cache import cache
from django.conf import settings
from TaqnyatSms import client
from login.models import OtpMessage
import json
import time



class ActionLoggingMixin:
    def log_action(self, user, action_type, model_name, instance_id=None, description=None):
        if isinstance(user, AnonymousUser):
            # Optionally, handle anonymous users differently, e.g., log a specific message or skip logging
            user = None  # or set a default user or placeholder
            description = description or f"{action_type} for {model_name} by anonymous"
        else:
            description = description or f"{action_type} for {model_name}"

        ActionLog.objects.create(
            user=user,
            action_type=action_type,
            description=description,
            timestamp=now()
        )
        
def send_message(phone_number, request_details, test_mode=False):
    """
    Function to send a notification to the requester with the request details.
    """
    if test_mode:
        body = f"""
        TEST MODE: Your request has been created with the following details:
        - Housekeeper: {request_details['housekeeper']}
        - Requester Contact: {request_details['requester_contact']}
        - Request Date: {request_details['request_date']}
        - Duration: {request_details['duration']}
        - Price: {request_details['total_price']}
        - Status: {request_details['status']}
        """
        # Return success immediately in test mode
        return True, "Test mode: Message simulated successfully."
    
    body = f"""
    Your request has been created with the following details:
    - Housekeeper: {request_details['housekeeper']}
    - Requester Contact: {request_details['requester_contact']}
    - Request Date: {request_details['request_date']}
    - Duration: {request_details['duration']}
    - Price: {request_details['total_price']}
    - Status: {request_details['status']}
    """
    
    sender = 'OFAQ'
    scheduled = None  # Optional: Set this if you want to schedule the message

    print(f"Sending message to {phone_number}: {body}")  # Debug statement

    try:
        taqnyt = client(settings.TAQNYAT_API_KEY)
        response = taqnyt.sendMsg(body, [phone_number], sender, scheduled)
        
        response_data = json.loads(response)
        
        if response_data.get('status') == 'success':
            return True, "Message sent successfully."
        else:
            error_message = response_data.get('message', 'Unknown error')
            print(f"Failed to send notification: {error_message}")  # Debug statement
            return False, f"Failed to send notification: {error_message}"
    except Exception as e:
        print(f"Error sending message: {e}")  # Debug statement
        return False, f"Error sending message: {e}"
