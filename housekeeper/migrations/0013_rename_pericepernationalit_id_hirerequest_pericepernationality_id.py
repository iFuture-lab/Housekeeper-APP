# Generated by Django 5.0.7 on 2024-08-01 08:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('housekeeper', '0012_hirerequest_duration_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hirerequest',
            old_name='pericepernationalit_id',
            new_name='pericepernationality_id',
        ),
    ]
