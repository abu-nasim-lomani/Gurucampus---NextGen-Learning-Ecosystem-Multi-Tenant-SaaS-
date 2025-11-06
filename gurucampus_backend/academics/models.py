# academics/models.py
from django.db import models
from django.conf import settings

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
        
        # --- ফিক্স ২ (Deep Analysis): একটি ব্যাচ অবশ্যই একটি ডিপার্টমেন্টের অংশ।
        # যদি ডিপার্টমেন্ট ডিলিট হয়, তবে ব্যাচও ডিলিট হওয়া উচিত।
        # তাই on_delete=models.CASCADE ব্যবহার করা হলো।
        on_delete=models.CASCADE, 
        
        # --- ফিক্স ১ (The Error): 'courses' থেকে 'batches'-এ পরিবর্তন করা হলো
        # এটি 'courses.Course' মডেলের সাথে ক্ল্যাশ (clash) সমাধান করবে।
        related_name="batches"
    )
    name = models.CharField(max_length=255) # e.g., "E-101" or "49th Batch"
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True) # ব্যাচের শেষ তারিখ ঐচ্ছিক হতে পারে

    def __str__(self):
        # department এখন null হতে পারে না, তাই এই কোডটি নিরাপদ।
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
    """
    course = models.ForeignKey(
        "courses.Course",  # স্ট্রিং নোটেশন ঠিক আছে
        on_delete=models.CASCADE, 
        related_name="classes"
    )
    batch = models.ForeignKey(
        # --- ফিক্স ৩ (Best Practice): সামঞ্জস্যের জন্য স্ট্রিং নোটেশন ব্যবহার করা হলো
        "academics.Batch", 
        on_delete=models.CASCADE, 
        related_name="classes"
    )
    semester = models.ForeignKey(
        # --- ফিক্স ৩ (Best Practice): সামঞ্জস্যের জন্য স্ট্রিং নোটেশন ব্যবহার করা হলো
        "academics.Semester", 
        on_delete=models.CASCADE, 
        related_name="classes"
    )
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="classes_taught"
    )
    invite_code = models.CharField(max_length=20, unique=True, blank=True, null=True)
    
    def __str__(self):
        # এই __str__ মেথডটি এখন কাজ করবে, কারণ সব মডেল ঠিকভাবে লিঙ্ক করা আছে।
        # তবে, এটি অনেকগুলো ডেটাবেস কোয়েরি করতে পারে। আমরা পরে এটি অপ্টিমাইজ করবো।
        try:
            return f"{self.course.title} ({self.batch.name}) - {self.semester.name}"
        except Exception:
            return f"Class ID: {self.id} (Incomplete Data)"