import os
import django
import yaml
from django.db.models import Field

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_project.settings')
django.setup()

from django.apps import apps

def get_model_schema():
    schema = {}
    for model in apps.get_models():
        model_name = model.__name__.lower()
        model_fields = []
        
        for field in model._meta.get_fields():
            if isinstance(field, Field):
                field_info = {
                    'name': field.name,
                    'type': field.get_internal_type()
                }
                model_fields.append(field_info)
        
        # Only add to schema if fields are found
        if model_fields:
            schema[model_name] = model_fields
        else:
            schema[model_name] = 'No fields found'  # Debugging line
        
    return schema

def save_schema_to_yaml(schema, file_path):
    with open(file_path, 'w') as file:
        yaml.dump(schema, file, default_flow_style=False)

if __name__ == "__main__":
    schema = get_model_schema()
    save_schema_to_yaml(schema, 'schema.yaml')
