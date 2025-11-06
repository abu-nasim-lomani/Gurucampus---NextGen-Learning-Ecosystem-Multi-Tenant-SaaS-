# assessments/models.py
from django.db import models
from django.conf import settings
from courses.models import Course # courses অ্যাপ থেকে Course মডেল ইম্পোর্ট করছি

class Assessment(models.Model):
    """
    একটি পরীক্ষা বা অ্যাসাইনমেন্ট (যেমন "Midterm Exam")
    """
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE, 
        related_name="assessments"
    )
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} (Course: {self.course.title})"

class Problem(models.Model):
    """
    অ্যাসাইনমেন্টের ভেতরের একটি নির্দিষ্ট কোডিং প্রবলেম।
    """
    assessment = models.ForeignKey(
        Assessment, 
        on_delete=models.CASCADE, 
        related_name="problems"
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True) # প্রবলেমের বিবরণ
    
    # ইন্সট্রাক্টর এই টেমপ্লেট কোডটি দেবেন, যা ছাত্ররা এডিটরে দেখবে
    template_code = models.TextField(blank=True, help_text="Starting code for the user")

    def __str__(self):
        return self.title
    
class TestCase(models.Model):
    """
    একটি প্রবলেমের জন্য গোপন টেস্ট কেস (Input/Output)।
    """
    problem = models.ForeignKey(
        Problem, 
        on_delete=models.CASCADE, 
        related_name="testcases"
    )
    input_data = models.TextField(blank=True, help_text="Standard input (stdin)")
    expected_output = models.TextField(help_text="Expected standard output (stdout)")
    
    # এই টেস্ট কেসটি কি ছাত্রকে দেখানো হবে? (নাকি গোপন থাকবে)
    is_hidden = models.BooleanField(default=True) 

    def __str__(self):
        return f"TestCase for {self.problem.title} (Hidden: {self.is_hidden})"


class Submission(models.Model):
    """
    একটি প্রবলেমের জন্য ছাত্রের কোড সাবমিশন।
    """
    problem = models.ForeignKey(
        Problem, 
        on_delete=models.CASCADE, 
        related_name="submissions"
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="submissions"
    )
    submitted_code = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Autograder (Judge0) এই স্ট্যাটাসগুলো সেট করবে
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Accepted', 'Accepted'),
        ('Wrong Answer', 'Wrong Answer'),
        ('Time Limit Exceeded', 'Time Limit Exceeded'),
        ('Compilation Error', 'Compilation Error'),
        ('Runtime Error', 'Runtime Error'),
    ]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    
    # Judge0 থেকে প্রাপ্ত আউটপুট বা এরর
    output = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Submission by {self.student.username} for {self.problem.title} [{self.status}]"