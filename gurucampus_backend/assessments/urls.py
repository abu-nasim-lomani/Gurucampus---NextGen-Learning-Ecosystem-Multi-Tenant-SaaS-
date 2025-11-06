# assessments/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AssessmentViewSet, 
    ProblemViewSet, 
    TestCaseViewSet,    # <-- Import this
    SubmissionViewSet   # <-- Import this
)

# DRF Router setup
router = DefaultRouter()
router.register(r'assessments', AssessmentViewSet, basename='assessment')
router.register(r'problems', ProblemViewSet, basename='problem')
router.register(r'testcases', TestCaseViewSet, basename='testcase')     # <-- Add this line
router.register(r'submissions', SubmissionViewSet, basename='submission') # <-- Add this line

urlpatterns = [
    path('', include(router.urls)),
]