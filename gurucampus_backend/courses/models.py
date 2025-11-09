from django.db import models
# We no longer need to import 'academics.models'
# We will use string notation for all ForeignKeys to other apps

class Course(models.Model):
    """
    Represents a Course "Blueprint" or "Subject" (e.g., "Networking").
    (This is the CORRECT "TENANT_APP" architecture)
    """
    
    # We link to "academics.Department" using a string
    department = models.ForeignKey(
        "academics.Department",
        on_delete=models.SET_NULL,
        null=True,
        related_name="courses"
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    
    # B2C Price Fields
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00,
        help_text="Price for B2C marketplace. 0.00 for B2B."
    )
    is_b2c_public = models.BooleanField(
        default=False,
        help_text="Is this course available for purchase on the B2C marketplace?"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Module(models.Model):
    """
    A module or "chapter" of a Course Blueprint.
    """
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE, 
        related_name="modules"
    )
    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

class Lesson(models.Model):
    """
    A single lesson within a Module.
    Supports all "world-class" content types.
    """
    module = models.ForeignKey(
        Module, 
        on_delete=models.CASCADE, 
        related_name="lessons"
    )
    
    LESSON_TEXT = 'Text'
    LESSON_VIDEO = 'Video'
    LESSON_FILE = 'File'
    LESSON_PRACTICE = 'Practice'
    LESSON_TYPE_CHOICES = [
        (LESSON_TEXT, 'Text Content (Office Word-like)'),
        (LESSON_VIDEO, 'Video (YouTube/Vimeo)'),
        (LESSON_FILE, 'File (PDF/Slides)'),
        (LESSON_PRACTICE, 'Practice (Quiz or Coding Problem)'),
    ]
    
    title = models.CharField(max_length=255)
    lesson_type = models.CharField(
        max_length=20, 
        choices=LESSON_TYPE_CHOICES, 
        default=LESSON_TEXT
    )
    order = models.PositiveIntegerField(default=0)

    # Content Fields
    text_content = models.TextField(blank=True, null=True) 
    video_url = models.URLField(blank=True, null=True)
    file_upload = models.FileField(upload_to='lessons/files/', blank=True, null=True)
    
    # "Practice" link (This is the "world-class" integration)
    practice = models.ForeignKey(
        'assessments.Assessment', # String notation is correct
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text="Select an assessment or quiz for this lesson."
    )

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.module.title} - {self.title}"