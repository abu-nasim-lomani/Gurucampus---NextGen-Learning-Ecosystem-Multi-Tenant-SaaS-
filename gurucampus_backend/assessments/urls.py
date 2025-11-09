# assessments/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AssessmentViewSet, 
    ProblemViewSet, 
    TestCaseViewSet, 
    SubmissionViewSet,
    QuizQuestionViewSet,  
    QuizAttemptViewSet  
)

# DRF Router setup
router = DefaultRouter()
router.register(r'assessments', AssessmentViewSet, basename='assessment')
router.register(r'problems', ProblemViewSet, basename='problem')
router.register(r'testcases', TestCaseViewSet, basename='testcase') 
router.register(r'submissions', SubmissionViewSet, basename='submission') 
router.register(r'quiz-questions', QuizQuestionViewSet, basename='quizquestion') 
router.register(r'quiz-attempts', QuizAttemptViewSet, basename='quizattempt')

urlpatterns = [
    path('', include(router.urls)),
]