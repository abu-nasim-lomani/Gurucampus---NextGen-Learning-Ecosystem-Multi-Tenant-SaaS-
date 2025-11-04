# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# আমাদের CustomUser মডেলটিকে অ্যাডমিন সাইটে রেজিস্টার করছি
admin.site.register(CustomUser, UserAdmin)