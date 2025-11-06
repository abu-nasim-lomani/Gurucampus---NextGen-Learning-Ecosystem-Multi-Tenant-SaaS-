# academics/views.py
from rest_framework import viewsets
from .models import Department, Batch, Semester, Class
from .serializers import (
    DepartmentSerializer, 
    BatchSerializer, 
    SemesterSerializer, 
    ClassSerializer
)

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
    # Allow filtering by department, e.g., /api/v1/batches/?department=1
    filterset_fields = ['department']

class SemesterViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Semesters.
    """
    queryset = Semester.objects.all()
    serializer_class = SemesterSerializer
    # Allow filtering for active semesters, e.g., /api/v1/semesters/?is_active=true
    filterset_fields = ['is_active']

class ClassViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Classes (the "Live Classroom").
    """
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    # Allow filtering by all key relationships
    filterset_fields = ['course', 'batch', 'semester', 'teacher']