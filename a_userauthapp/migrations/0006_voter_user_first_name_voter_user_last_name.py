# Generated by Django 5.2.1 on 2025-05-25 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a_userauthapp', '0005_voter_user_is_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='voter_user',
            name='first_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='voter_user',
            name='last_name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
