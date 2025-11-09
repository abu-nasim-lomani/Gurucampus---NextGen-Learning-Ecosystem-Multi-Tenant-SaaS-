# marketplace/admin.py
from django.contrib import admin
from .models import InstructorApplication, InstructorProfile, Order

@admin.register(InstructorApplication)
class InstructorApplicationAdmin(admin.ModelAdmin):
    """
    "ওয়ার্ল্ড-ক্লাস" অ্যাডমিন: ইন্সট্রাক্টরদের আবেদনপত্র রিভিউ করার জন্য।
    """
    list_display = ('user', 'full_name', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('full_name', 'user__email')
    
    # অ্যাডমিন প্যানেল থেকে স্ট্যাটাস পরিবর্তন করার সুবিধা
    list_editable = ('status',)

@admin.register(InstructorProfile)
class InstructorProfileAdmin(admin.ModelAdmin):
    """
    অনুমোদিত ইন্সট্রাক্টরদের প্রোফাইল এবং Revenue Share ম্যানেজ করার জন্য।
    """
    list_display = ('user', 'revenue_share_percentage', 'paypal_email')
    search_fields = ('user__username',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    B2C (মার্কেটপ্লেস) বিক্রির হিসাব বা "লেজার বুক"।
    """
    list_display = ('id', 'student', 'course', 'final_price', 'instructor_share', 'platform_share', 'payment_status')
    list_filter = ('payment_status', 'course')
    search_fields = ('student__username', 'course__title')