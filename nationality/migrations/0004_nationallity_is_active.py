# Generated by Django 5.0.7 on 2024-08-10 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nationality', '0003_alter_nationallity_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='nationallity',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
