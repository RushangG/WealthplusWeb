# Generated by Django 4.2.11 on 2024-03-27 08:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_remove_userprofile_birthdate_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='password',
        ),
    ]