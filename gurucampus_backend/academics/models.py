# academics/models.py
from django.db import models
from django.conf import settings
import secrets  # <-- Your "world-class" auto-generation library

class Department(models.Model):
    """
    Represents an academic department, e.g., "CSE" or "BBA".
    Each department belongs to the tenant.
    """
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Batch(models.Model):
    """
    Represents a group of students, e.g., "E-101".
    This is linked to a department.
    """
    department = models.ForeignKey(
        "academics.Department",
        on_delete=models.CASCADE, 
        related_name="batches"
    )
    name = models.CharField(max_length=255) # e.g., "E-101" or "49th Batch"
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.department.name})"

class Semester(models.Model):
    """
    Represents an academic period, e.g., "Fall 2025" or "6th Semester".
    """
    name = models.CharField(max_length=255) # e.g., "6th Semester" or "Fall 2025"
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    
class Class(models.Model):
    """
    The "Live Classroom" or "Section".
    (Updated to auto-generate invite codes)
    """
    course = models.ForeignKey(
        "courses.Course",  # String notation is correct
        on_delete=models.CASCADE, 
        related_name="classes"
    )
    batch = models.ForeignKey(
        "academics.Batch", # String notation is correct
        on_delete=models.CASCADE, 
        related_name="classes"
    )
    semester = models.ForeignKey(
        "academics.Semester", # String notation is correct
        on_delete=models.CASCADE, 
        related_name="classes"
    )
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="classes_taught"
    )
    
    # --- THIS IS THE UPDATE ---
    # We will auto-generate this code. 
    # max_length=10 is safe for our 8-char token.
    invite_code = models.CharField(max_length=20, unique=True, blank=True, null=True)
    
    def __str__(self):
        try:
            return f"{self.course.title} ({self.batch.name}) - {self.semester.name}"
        except Exception:
            return f"Class ID: {self.id} (Incomplete Data)"

    # --- THIS IS THE "WORLD-CLASS" LOGIC YOU REQUESTED ---
    def save(self, *args, **kwargs):
        """
        Override save to auto-generate a unique invite code.
        """
        if not self.invite_code:
            # Generate a unique, 8-character, URL-safe code
            self.invite_code = secrets.token_urlsafe(8)
            
            # Ensure it's truly unique
            while Class.objects.filter(invite_code=self.invite_code).exists():
                self.invite_code = secrets.token_urlsafe(8)
                
        super().save(*args, **kwargs) # Call the original save method
            
            
class ClassroomMember(models.Model):
    """
    Connects a User to a Class (the "Waiting Room").
    This manages roles (Student/Teacher) and status (Pending/Active).
    """
    
    # --- Role Choices ---
    ROLE_STUDENT = 'Student'
    ROLE_TEACHER = 'Teacher'
    ROLE_CHOICES = [
        (ROLE_STUDENT, 'Student'),
        (ROLE_TEACHER, 'Teacher'),
    ]

    # --- Status Choices (The Security Logic) ---
    STATUS_PENDING = 'Pending'
    STATUS_ACTIVE = 'Active'
    STATUS_REJECTED = 'Rejected'
    STATUS_INACTIVE = 'Inactive'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),   # In the waiting room
        (STATUS_ACTIVE, 'Active'),     # Approved by teacher
        (STATUS_REJECTED, 'Rejected'), # Rejected by teacher
        (STATUS_INACTIVE, 'Inactive'), # Semester ended
    ]

    # --- Model Fields ---
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="class_memberships"
    )
    classroom = models.ForeignKey(
        "academics.Class",
        on_delete=models.CASCADE,
        related_name="members"
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_STUDENT)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # A user can only join a class once
        unique_together = ('user', 'classroom')

    def __str__(self):
        return f"{self.user.username} as {self.role} in {self.classroom_id} ({self.status})"