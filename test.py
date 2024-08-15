from django.conf import settings
import os

def check_template_path():
    template_name = 'contract_Recruitment.docx'
    template_path = os.path.join(settings.BASE_DIR, 'templates', template_name)
    if os.path.exists(template_path):
        print(f"Template found at: {template_path}")
    else:
        print(f"Template not found at: {template_path}")

check_template_path()