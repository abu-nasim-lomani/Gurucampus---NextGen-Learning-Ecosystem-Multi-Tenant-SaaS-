# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):

    student_id = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        help_text="e.g., E-101-049. Used for teacher verification."
    )
    
    phone = models.CharField(
        max_length=20, 
        blank=True, 
        null=True,
        help_text="Student's contact phone number"
    )
    date_of_birth = models.DateField(
        blank=True, 
        null=True,
        help_text="Student's date of birth"
    )
    