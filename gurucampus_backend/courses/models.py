# courses/models.py
from django.db import models
from django.conf import settings

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    
    # প্রতিটি কোর্সের একজন 'মালিক' (ইন্সট্রাক্টর) থাকবে।
    # আমরা settings.AUTH_USER_MODEL ব্যবহার করছি যা 'users.CustomUser'-কে নির্দেশ করে।
    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="courses_taught"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title