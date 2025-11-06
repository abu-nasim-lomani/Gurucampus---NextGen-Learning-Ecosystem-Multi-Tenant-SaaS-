# assessments/serializers.py
from rest_framework import serializers
from .models import Assessment, Problem, Submission, TestCase

class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = [
            'id', 
            'title', 
            'description', 
            'template_code', 
            'assessment'
        ]

class AssessmentSerializer(serializers.ModelSerializer):
    # একটি Assessment-এর ভেতরের সব Problem দেখানোর জন্য
    problems = ProblemSerializer(many=True, read_only=True)

    class Meta:
        model = Assessment
        fields = [
            'id', 
            'title', 
            'course', 
            'created_at', 
            'problems' # নেস্টেড প্রবলেমগুলো এখানে দেখাবে
        ]
        
        
class TestCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCase
        fields = [
            'id', 
            'problem', 
            'input_data', 
            'expected_output', 
            'is_hidden'
        ]


class SubmissionSerializer(serializers.ModelSerializer):
    # 'student'-কে read_only করছি, কারণ এটি রিকোয়েস্টকারী ইউজার থেকে সেট হবে
    student = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Submission
        fields = [
            'id', 
            'problem', 
            'student', 
            'submitted_code', 
            'status', 
            'output', 
            'timestamp'
        ]
        
        # 'status' এবং 'output' শুধুমাত্র Autograder পরিবর্তন করতে পারবে,
        # ইউজার নিজে নয়।
        read_only_fields = ['status', 'output', 'student']