# utils.py
from django.utils.timezone import now
from .models import ActionLog
from django.contrib.auth.models import AnonymousUser
from .models import CustomUser

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
   