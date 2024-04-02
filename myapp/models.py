from django.db import models
from django.contrib.auth.models import User




class UserProfile(models.Model):     
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None, null=True)

    username = models.CharField(max_length=100 , default="user")
    email = models.EmailField()
    address = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=15)
    GENDER_CHOICES = [('M', 'Male'),('F', 'Female'),('O', 'Other')]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)





class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True)
    source = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    date = models.DateField(default='2000-01-01')
    category = models.CharField(max_length=100, default='Other')

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True)
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    date = models.DateField(default='2000-01-01')
    category = models.CharField(max_length=100, default='Other')

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None, null=True)
    role = models.CharField(max_length=50, default='admin')
    is_active = models.BooleanField(default=True)


class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True)
    username = models.CharField(max_length=150, blank=True, null=True)  # Field to store username separately
    total_income = models.DecimalField(max_digits=25, decimal_places=2, default=0.00)
    total_expense = models.DecimalField(max_digits=25, decimal_places=2, default=0.00)
    profit = models.DecimalField(max_digits=25, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
