# Generated by Django 5.0.7 on 2024-08-01 07:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('housekeeper', '0011_employmenttype_religion_housekeeper_gender_and_more'),
        ('perice_per_nationality', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hirerequest',
            name='duration',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='hirerequest',
            name='pericepernationalit_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='perice_per_nationality.pericepernationality'),
        ),
        migrations.AddField(
            model_name='hirerequest',
            name='total_price',
            field=models.FloatField(default=0.0),
        ),
    ]
