# academics/views.py
from rest_framework.views import APIView
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
# from rest_framework.decorators import action  <- We no longer need this
from tenants.models import Organization # <-- Required for the user limit check
from .models import Department, Batch, Semester, Class, ClassroomMember
from .serializers import (
    DepartmentSerializer, 
    BatchSerializer, 
    SemesterSerializer, 
    ClassSerializer,
    ClassroomMemberSerializer,
    ClassroomMemberManageSerializer
)
from django.shortcuts import get_object_or_404

class DepartmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Departments.
    """
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class BatchViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Batches.
    """
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer
    filterset_fields = ['department']

class SemesterViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Semesters.
    """
    queryset = Semester.objects.all()
    serializer_class = SemesterSerializer
    filterset_fields = ['is_active']

class ClassViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Classes (the "Live Classroom").
    """
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    filterset_fields = ['course', 'batch', 'semester', 'teacher']
    
class ClassroomMemberViewSet(viewsets.ModelViewSet):
    """
    API endpoint for the "Waiting Room" (Classroom Members).
    """
    queryset = ClassroomMember.objects.all()
    serializer_class = ClassroomMemberSerializer
    filterset_fields = ['classroom', 'status', 'role']

    def perform_create(self, serializer):
        """
        Automatically set the student to the current logged-in user
        and set the initial status to 'Pending'.
        """
        serializer.save(
            user=self.request.user, 
            status=ClassroomMember.STATUS_PENDING
        )

# --- This is the UPDATED View with User Limit Logic ---
class ManageMemberView(APIView):
    """
    A standalone, secure API view for a teacher to Approve/Reject a student.
    (Now includes "User Limit Enforcement")
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Get the class ID from the URL
        class_pk = self.kwargs.get('class_pk')
        classroom = get_object_or_404(Class, pk=class_pk)

        # --- Security Check 1: Is the user the teacher? ---
        if classroom.teacher != request.user:
            return Response(
                {"detail": "You are not the teacher of this class."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Validate the incoming data ({ "member_id": 1, "action": "Active" })
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

        ### --- START: "WORLD-CLASS" USER LIMIT LOGIC --- ###
        
        # We only check the limit if the teacher is trying to "Activate" a student
        if new_status == ClassroomMember.STATUS_ACTIVE and member.status != ClassroomMember.STATUS_ACTIVE:
            
            # 1. Get the current tenant (e.g., 'brac')
            tenant = request.tenant
            
            # 2. Get the purchased user limit for this tenant
            user_limit = tenant.user_limit
            
            # 3. Check if the plan is "Unlimited" (we use -1 for unlimited)
            if user_limit != -1:
                
                # 4. Count the current number of active students in this tenant
                # This query automatically runs only on the 'brac' schema
                current_active_students = ClassroomMember.objects.filter(
                    status=ClassroomMember.STATUS_ACTIVE,
                    role=ClassroomMember.ROLE_STUDENT
                ).count()
                
                # 5. Enforce the limit
                if current_active_students >= user_limit:
                    return Response(
                        {"detail": f"User Limit Reached. Your plan allows {user_limit} active students."},
                        status=status.HTTP_403_FORBIDDEN
                    )
        ### --- END: USER LIMIT LOGIC --- ###

        # --- The Action: Update the student's status ---
        member.status = new_status
        member.save()

        return Response(
            {"detail": f"Student status updated to {new_status}."},
            status=status.HTTP_200_OK
        )