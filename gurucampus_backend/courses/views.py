# courses/views.py
from rest_framework import viewsets, permissions
from .models import Course
from .serializers import CourseSerializer

class CourseViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing courses.
    """
    queryset = Course.objects.all().order_by('-created_at')
    serializer_class = CourseSerializer
    
    # শুধুমাত্র লগইন করা ইউজাররাই কোর্স দেখতে বা তৈরি করতে পারবে।
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        কোর্স তৈরি করার সময় রিকোয়েস্টকারী ইউজারকে 
        স্বয়ংক্রিয়ভাবে 'instructor' হিসেবে সেট করে।
        """
        serializer.save(instructor=self.request.user)