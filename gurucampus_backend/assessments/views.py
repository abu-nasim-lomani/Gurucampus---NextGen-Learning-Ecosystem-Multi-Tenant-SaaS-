# assessments/views.py
from rest_framework import viewsets, permissions, status

from rest_framework.response import Response
from .models import (
    Assessment, Problem, TestCase, Submission,
    QuizQuestion, QuizAttempt
)
from academics.models import Class, ClassroomMember
from .serializers import (
    AssessmentSerializer, 
    ProblemSerializer, 
    TestCaseSerializer, 
    SubmissionSerializer,
    QuizAttemptSerializer,
    QuizQuestionTeacherSerializer, # <-- Correct import
    QuizQuestionStudentSerializer  # <-- Correct import
)
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from .tasks import grade_submission

# (AssessmentViewSet remains unchanged)
class AssessmentViewSet(viewsets.ModelViewSet):
    queryset = Assessment.objects.all().order_by('-created_at')
    serializer_class = AssessmentSerializer

# (ProblemViewSet remains unchanged)
class ProblemViewSet(viewsets.ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
    filterset_fields = ['assessment']

# (TestCaseViewSet remains unchanged)
class TestCaseViewSet(viewsets.ModelViewSet):
    queryset = TestCase.objects.all()
    serializer_class = TestCaseSerializer
    filterset_fields = ['problem']

# (SubmissionViewSet is correct)
class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all().order_by('-timestamp')
    serializer_class = SubmissionSerializer
    filterset_fields = ['problem', 'student']

    def perform_create(self, serializer):
        submission = serializer.save(student=self.request.user)
        schema_name = self.request.tenant.schema_name
        grade_submission.delay(submission.id, schema_name)

# --- THE DUPLICATE FUNCTION THAT WAS HERE IS NOW REMOVED ---


class QuizQuestionViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Quiz Questions.
    (NOW SECURED with Role-Based Permissions)
    """
    queryset = QuizQuestion.objects.all()
    filterset_fields = ['assessment']

    # --- এটিই "ওয়ার্ল্ড-ক্লাস" সিকিউরিটি ফিক্স ---
    def get_permissions(self):
        """
        Installs appropriate permission classes.
        - GET (list, retrieve): Any authenticated user can see.
        - POST, PUT, DELETE: Only admin/staff (teachers) can do.
        """
        if self.action in ['list', 'retrieve']:
            # ছাত্ররা প্রশ্ন দেখতে (GET) পারবে
            return [permissions.IsAuthenticated()]
        
        # কিন্তু শুধুমাত্র টিচাররা (is_staff=True) প্রশ্ন তৈরি/এডিট/ডিলিট (POST/PUT/DELETE) করতে পারবে
        return [permissions.IsAdminUser()]
    def get_serializer_class(self):
        # If the user is a teacher or admin
        if self.request.user.is_staff:
            return QuizQuestionTeacherSerializer
        
        # Otherwise (if a student)
        return QuizQuestionStudentSerializer

# (QuizAttemptViewSet is correct)
class QuizAttemptViewSet(viewsets.ModelViewSet):
    """
    API endpoint for students to submit Quiz Answers.
    This view will grade the answer immediately.
    """
    queryset = QuizAttempt.objects.all().order_by('-timestamp')
    serializer_class = QuizAttemptSerializer
    filterset_fields = ['question', 'student']

    def perform_create(self, serializer):
        """
        Automatically set the student and grade the answer.
        This is the "instant grading" logic.
        """
        question = serializer.validated_data['question']
        
        is_correct = (
            question.correct_answer.lower() == 
            serializer.validated_data['selected_answer'].lower()
        )
        
        serializer.save(
            student=self.request.user, 
            is_correct=is_correct
        )

# (ManageMemberView is correct)
class ManageMemberView(APIView):
    """
    A standalone, secure API view for a teacher to Approve/Reject a student.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        class_pk = self.kwargs.get('class_pk')
        classroom = get_object_or_404(Class, pk=class_pk)

        # --- Security Check 1: Is the user the teacher? ---
        if classroom.teacher != request.user:
            return Response(
                {"detail": "You are not the teacher of this class."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Validate data
        serializer = ClassroomMemberManageSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        member_id = serializer.validated_data['member_id']
        new_status = serializer.validated_data['action']

        try:
            # --- Security Check 2: Is the member in this class? ---
            member = get_object_or_404(
                ClassroomMember, 
                id=member_id, 
                classroom=classroom
            )
        except ClassroomMember.DoesNotExist:
            return Response(
                {"detail": "This member is not part of this class."},
                status=status.HTTP_404_NOT_FOUND
            )

        # --- The Action: Update the status ---
        member.status = new_status
        member.save()

        return Response(
            {"detail": f"Student status updated to {new_status}."},
            status=status.HTTP_200_OK
        )