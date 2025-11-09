# assessments/serializers.py
from rest_framework import serializers
from .models import Assessment, Problem, Submission, TestCase
from .models import QuizQuestion, QuizAttempt
# (users.serializers.UserSerializer এখানে দরকার নেই, এটি academics-এ দরকার)

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
    problems = ProblemSerializer(many=True, read_only=True)
    class Meta:
        model = Assessment
        fields = [
            'id', 
            'title', 
            'course', 
            'created_at', 
            'problems'
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
        read_only_fields = ['status', 'output', 'student']

class QuizQuestionTeacherSerializer(serializers.ModelSerializer):
    """
    FOR TEACHERS: Serializer for creating/editing Quiz Questions.
    """
    class Meta:
        model = QuizQuestion
        fields = [
            'id', 
            'assessment', 
            'question_type', 
            'question_text', 
            'options',
            'correct_answer'
        ]

class QuizQuestionStudentSerializer(serializers.ModelSerializer):
    """
    FOR STUDENTS: Serializer for viewing Quiz Questions.
    """
    class Meta:
        model = QuizQuestion
        fields = [
            'id', 
            'assessment', 
            'question_type', 
            'question_text', 
            'options'
        ]

# --- এই ক্লাসটিই অনুপস্থিত ছিল (THE MISSING PIECE) ---
class QuizAttemptSerializer(serializers.ModelSerializer):
    """
    Serializer for a student submitting an answer.
    """
    class Meta:
        model = QuizAttempt
        fields = [
            'id', 
            'question', 
            'selected_answer', 
            'is_correct', 
            'timestamp'
        ]
        read_only_fields = ['is_correct', 'timestamp']