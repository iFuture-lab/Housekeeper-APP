# Generated by Django 5.0.7 on 2024-07-25 06:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0010_alter_customuser_phone_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='is_superuser',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='user_permissions',
        ),
    ]
