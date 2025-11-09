# courses/views.py
from rest_framework import viewsets
from .models import Course, Module, Lesson  # <-- Import Module and Lesson
from .serializers import CourseSerializer, ModuleSerializer, LessonSerializer  # <-- Import new serializers
from academics.models import ClassroomMember, Class
from django.db.models import Q

class CourseViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing courses.
    (NOW SECURED: Students can only see courses they are enrolled in)
    """
    serializer_class = CourseSerializer
    
    def get_queryset(self):
        """
        "ওয়ার্ল্ড-ক্লাস" সিকিউরিটি:
        এই ইউজার (ছাত্র বা শিক্ষক) যে ক্লাসগুলোতে 'Active' আছেন,
        শুধু সেই ক্লাসগুলোর সাথেই যুক্ত কোর্সগুলো দেখান।
        """
        user = self.request.user

        # A. If the user is staff (teacher/admin), show all courses
        if user.is_staff:
            return Course.objects.all().order_by('-created_at')

        # B. If the user is a normal student
        
        # 1. Find all "Active" class memberships for this student
        active_class_ids = ClassroomMember.objects.filter(
            user=user,
            status=ClassroomMember.STATUS_ACTIVE
        ).values_list('classroom_id', flat=True)

        # 2. Find all "Courses" (blueprints) linked to those active classes
        course_ids = Class.objects.filter(
            id__in=active_class_ids
        ).values_list('course_id', flat=True)

        # 3. Return only that specific list of courses
        return Course.objects.filter(id__in=course_ids).order_by('-created_at')

# --- These are the new ViewSets for your Syllabus ---

class ModuleViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Modules.
    Teachers POST/PUT to create/edit modules.
    Students GET to see them (if they are in the class).
    """
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    # Allow filtering by course
    filterset_fields = ['course']

class LessonViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Lessons.
    Teachers POST/PUT to create/edit lessons.
    Students GET to see them (if they are in the class).
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    # Allow filtering by module
    filterset_fields = ['module']