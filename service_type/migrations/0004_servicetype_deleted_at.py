# Generated by Django 5.0.7 on 2024-08-17 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service_type', '0003_servicetype_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicetype',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
