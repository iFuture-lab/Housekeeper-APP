# Generated by Django 5.0.7 on 2024-08-17 07:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0005_alter_contract_payment_details'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contract',
            name='deleted_at',
        ),
    ]
