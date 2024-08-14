# Generated by Django 5.0.7 on 2024-08-14 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('role', '0002_alter_role_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='role',
            name='permissions',
            field=models.ManyToManyField(related_name='roles', to='role.permission'),
        ),
    ]
