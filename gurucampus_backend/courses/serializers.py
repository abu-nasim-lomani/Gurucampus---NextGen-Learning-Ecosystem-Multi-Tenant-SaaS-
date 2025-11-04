# courses/serializers.py
from rest_framework import serializers
from .models import Course

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            'id', 
            'title', 
            'description', 
            'instructor', 
            'created_at'
        ]
        
        # আমরা 'instructor' ফিল্ডটিকে 'read_only' করছি।
        # এর মানে হলো, কোর্স তৈরি করার সময় আমরা রিকোয়েস্ট করা 
        # ইউজারকে স্বয়ংক্রিয়ভাবে ইন্সট্রাক্টর হিসেবে সেট করবো, 
        # ইউজার নিজে এটি সেট করতে পারবে না।
        read_only_fields = ['instructor']