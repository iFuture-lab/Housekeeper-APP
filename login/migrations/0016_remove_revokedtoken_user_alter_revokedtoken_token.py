# Generated by Django 5.0.7 on 2024-08-01 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0015_revokedtoken'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='revokedtoken',
            name='user',
        ),
        migrations.AlterField(
            model_name='revokedtoken',
            name='token',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
