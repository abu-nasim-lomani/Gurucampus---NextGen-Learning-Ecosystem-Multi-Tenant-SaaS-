# courses/models.py
from django.db import models
# We are removing the 'settings' import as we no longer need AUTH_USER_MODEL here
from academics.models import Department # Import Department from our new app

class Course(models.Model):
    """
    Represents a Course "Blueprint" or "Subject" (e.g., "Networking").
    This is the master library of content, owned by a department.
    """
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL, # If dept is deleted, course remains
        null=True,
        related_name="courses"
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    
    # We have REMOVED the 'instructor' field.
    # The instructor is now on the 'Class' model.
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title