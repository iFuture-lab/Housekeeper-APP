# Generated by Django 5.0.7 on 2024-08-10 07:47

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0009_alter_payment_action'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
