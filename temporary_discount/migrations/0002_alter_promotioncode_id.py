# Generated by Django 5.0.7 on 2024-08-10 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('temporary_discount', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotioncode',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
