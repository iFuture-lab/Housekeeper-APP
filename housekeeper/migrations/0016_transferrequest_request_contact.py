# Generated by Django 5.0.7 on 2024-08-08 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('housekeeper', '0015_actionlog'),
    ]

    operations = [
        migrations.AddField(
            model_name='transferrequest',
            name='request_contact',
            field=models.CharField(default='0123456789', max_length=100),
        ),
    ]
