# Generated by Django 5.0.2 on 2024-03-08 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_userprofile_password1'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='password2',
            field=models.CharField(default='12345678', max_length=20),
        ),
    ]
