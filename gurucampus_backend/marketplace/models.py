# marketplace/models.py
from django.db import models
from django.conf import settings

# === 1. The "Waiting Room" for Teachers ===
# This is your "secure, modern, professional" vetting model

class InstructorApplication(models.Model):
    """
    Handles the application for a user to become an instructor.
    This is the "Quality Gating" step.
    """
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    
    # The user who is applying
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="instructor_application"
    )
    
    # --- Verification Fields (as we discussed) ---
    full_name = models.CharField(max_length=255)
    linkedin_profile_url = models.URLField(max_length=500)
    sample_video_url = models.URLField(max_length=500, help_text="A 5-10 min unlisted video (YouTube/Vimeo)")
    teaching_experience = models.TextField(blank=True, null=True)
    
    # --- Admin Fields ---
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    admin_feedback = models.TextField(blank=True, null=True, help_text="Feedback for the applicant")
    
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Application for {self.user.username} ({self.status})"

# === 2. The "Contract" for Approved Teachers ===

class InstructorProfile(models.Model):
    """
    The "Contract". This is created *after* an application is approved.
    It flags a user as an instructor and stores their revenue share.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="instructor_profile"
    )
    
    # The percentage (e.g., 70.00) the instructor keeps from a sale
    revenue_share_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=70.00
    )
    
    # Bank details for payouts (can be encrypted later)
    paypal_email = models.EmailField(blank=True, null=True)
    
    def __str__(self):
        return f"Instructor Profile for {self.user.username}"

# === 3. The "Automated Cash Register" for B2C Sales ===

class Order(models.Model):
    """
    The "Ledger Book" or "Cash Register".
    Tracks a single B2C course purchase and calculates the revenue split.
    """
    # The student who bought the course
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, # If student is deleted, we keep the order
        null=True,
        related_name="b2c_orders"
    )
    
    # The course that was purchased
    course = models.ForeignKey(
    "courses.Course",  # <-- "app_name.ModelName"
    on_delete=models.SET_NULL,
    null=True,
    related_name="b2c_sales"
)
    
    # --- Payment & Revenue Share Fields ---
    final_price = models.DecimalField(max_digits=10, decimal_places=2)
    instructor_share = models.DecimalField(max_digits=10, decimal_places=2)
    platform_share = models.DecimalField(max_digits=10, decimal_places=2)
    
    payment_status = models.CharField(max_length=20, default='Pending') # e.g., 'Pending', 'Complete'
    payment_gateway_id = models.CharField(max_length=255, blank=True, null=True) # e.g., Stripe charge ID
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.student.username} for {self.course.title}"