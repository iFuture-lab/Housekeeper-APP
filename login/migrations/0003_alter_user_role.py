# Generated by Django 5.0.7 on 2024-07-24 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_alter_user_options_alter_user_managers_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(default='admin', max_length=150, unique=True),
        ),
    ]
