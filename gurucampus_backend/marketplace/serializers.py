# marketplace/serializers.py
from rest_framework import serializers
from .models import InstructorApplication, InstructorProfile, Order
from users.serializers import UserSerializer # ইন্সট্রাক্টরের তথ্য দেখানোর জন্য
from courses.serializers import CourseSerializer # কোর্সের তথ্য দেখানোর জন্য

class InstructorApplicationSerializer(serializers.ModelSerializer):
    """
    "ওয়ার্ল্ড-ক্লাস" আবেদনপত্র API:
    - ইন্সট্রাক্টররা এটি POST করে আবেদন করবেন।
    - সুপার অ্যাডমিন এটি GET করে রিভিউ করবেন।
    """
    # 'user' ফিল্ডটি read-only হবে এবং ইউজারের ডিটেইলস দেখাবে
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = InstructorApplication
        fields = [
            'id', 
            'user', 
            'full_name', 
            'linkedin_profile_url', 
            'sample_video_url', 
            'teaching_experience', 
            'status',
            'admin_feedback',
            'created_at'
        ]
        # 'status' এবং 'admin_feedback' শুধু সুপার অ্যাডমিন পরিবর্তন করতে পারবেন
        read_only_fields = ['status', 'admin_feedback', 'user']

class InstructorProfileSerializer(serializers.ModelSerializer):
    """
    সুপার অ্যাডমিনের জন্য: অনুমোদিত ইন্সট্রাক্টরদের প্রোফাইল
    """
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = InstructorProfile
        fields = ['id', 'user', 'revenue_share_percentage', 'paypal_email']

class OrderSerializer(serializers.ModelSerializer):
    """
    B2C "লেজার বুক" API: সমস্ত বিক্রির হিসাব
    """
    student = UserSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 
            'student', 
            'course', 
            'final_price', 
            'instructor_share', 
            'platform_share', 
            'payment_status',
            'created_at'
        ]