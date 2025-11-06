# assessments/views.py
from rest_framework import viewsets
from .models import Assessment, Problem, TestCase, Submission  # <-- Add TestCase, Submission
from .serializers import (
    AssessmentSerializer, 
    ProblemSerializer, 
    TestCaseSerializer, 
    SubmissionSerializer  # <-- Add TestCaseSerializer, SubmissionSerializer
)
from .tasks import grade_submission

# ... (AssessmentViewSet remains unchanged) ...
class AssessmentViewSet(viewsets.ModelViewSet):
    queryset = Assessment.objects.all().order_by('-created_at')
    serializer_class = AssessmentSerializer

# ... (ProblemViewSet remains unchanged) ...
class ProblemViewSet(viewsets.ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
    filterset_fields = ['assessment']


# --- Add these two new ViewSets below ---

class TestCaseViewSet(viewsets.ModelViewSet):
    """
    API endpoint for TestCases.
    Typically managed by instructors.
    """
    queryset = TestCase.objects.all()
    serializer_class = TestCaseSerializer
    
    # Filter by problem
    # e.g., /api/v1/testcases/?problem=1
    filterset_fields = ['problem']


class SubmissionViewSet(viewsets.ModelViewSet):
    """
    API endpoint for code Submissions.
    Used by students to submit code.
    """
    queryset = Submission.objects.all().order_by('-timestamp')
    serializer_class = SubmissionSerializer
    
    # Filter by problem or student
    filterset_fields = ['problem', 'student']

    def perform_create(self, serializer):
        """
        When a student submits code, automatically set the
        'student' field to the currently authenticated user.
        
        Then, trigger the background grading task.
        """
        # Save the submission first, with 'student' and default 'Pending' status
        submission = serializer.save(student=self.request.user)
        
        # Get the current tenant's schema name
        schema_name = self.request.tenant.schema_name
        
        # Send the grading job to Celery (the background worker)
        # .delay() is how you call a Celery task
        grade_submission.delay(submission.id, schema_name)

def perform_create(self, serializer):
    """
    When a student submits code, automatically set the
    'student' field to the currently authenticated user.

    Then, trigger the background grading task.
    """
    # Save the submission first, with 'student' and default 'Pending' status
    submission = serializer.save(student=self.request.user)

    # Get the current tenant's schema name
    schema_name = self.request.tenant.schema_name

    # Send the grading job to Celery (the background worker)
    # .delay() is how you call a Celery task
    grade_submission.delay(submission.id, schema_name)