# courses/serializers.py
from rest_framework import serializers
from .models import Course, Module, Lesson
# --- 1. Import the models we need to link ---
from assessments.models import Assessment 
from assessments.serializers import AssessmentSerializer 

# --- 2. This is the new, "World-Class" LessonSerializer ---
class LessonSerializer(serializers.ModelSerializer):
    """
    Serializer for a single Lesson.
    Handles both reading (nested) and writing (ID).
    """
    
    # FOR STUDENTS (GET): Show nested assessment details (read-only)
    practice = AssessmentSerializer(read_only=True)
    
    # FOR TEACHERS (POST/PUT): Accept just the Assessment ID (write-only)
    practice_id = serializers.PrimaryKeyRelatedField(
        queryset=Assessment.objects.all(),
        source='practice',  # This maps 'practice_id' to the 'practice' model field
        write_only=True,
        required=False,     # Not required if lesson_type is "Text"
        allow_null=True
    )
    
    class Meta:
        model = Lesson
        fields = [
            'id', 
            'title', 
            'lesson_type', 
            'order',
            'text_content',
            'video_url',
            'file_upload',
            'practice',      # This is for READING
            'practice_id',   # This is for WRITING
            'module',
        ]

# --- 3. The other serializers remain the same ---

class ModuleSerializer(serializers.ModelSerializer):
    """
    Serializer for a Module.
    It will show all Lessons nested inside it.
    """
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = [
            'id', 
            'title', 
            'order',
            'course',
            'lessons', # The list of lessons
        ]

class CourseSerializer(serializers.ModelSerializer):
    """
    Serializer for a Course.
    (Updated to show all Modules and B2C Price)
    """
    modules = ModuleSerializer(many=True, read_only=True)
    
    class Meta:
        model = Course
        fields = [
            'id', 
            'title', 
            'description', 
            'department',
            'created_at',
            'modules', # The list of modules
            
            # --- Add these two new B2C fields ---
            'price',
            'is_b2c_public',
            # ------------------------------------
        ]