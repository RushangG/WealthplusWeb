# Generated by Django 5.0.2 on 2024-02-17 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_admin_expense_financialreport_income_userprofile_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='admin',
            name='user',
        ),
        migrations.RemoveField(
            model_name='expense',
            name='user',
        ),
        migrations.RemoveField(
            model_name='financialreport',
            name='user',
        ),
        migrations.RemoveField(
            model_name='income',
            name='user',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='user',
        ),
        migrations.AddField(
            model_name='admin',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='admin',
            name='role',
            field=models.CharField(default='admin', max_length=50),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='address',
            field=models.CharField(default='Unknown', max_length=100),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='birthdate',
            field=models.DateField(default='2000-01-01'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(default='example@example.com', max_length=254),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(default='O', max_length=1),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='mobile_number',
            field=models.CharField(default='1234567890', max_length=15),
        ),
        migrations.AlterField(
            model_name='expense',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='expense',
            name='category',
            field=models.CharField(default='Other', max_length=100),
        ),
        migrations.AlterField(
            model_name='expense',
            name='date',
            field=models.DateField(default='2000-01-01'),
        ),
        migrations.AlterField(
            model_name='financialreport',
            name='report_date',
            field=models.DateField(default='2000-01-01'),
        ),
        migrations.AlterField(
            model_name='income',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='income',
            name='category',
            field=models.CharField(default='Other', max_length=100),
        ),
        migrations.AlterField(
            model_name='income',
            name='date',
            field=models.DateField(default='2000-01-01'),
        ),
    ]
