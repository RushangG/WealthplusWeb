# Inside admin.py in your myapp directory
from django.contrib import admin
from .models import UserProfile, Income, Expense,Report

admin.site.register(UserProfile)
admin.site.register(Income)
admin.site.register(Expense)
admin.site.register(Report)
