# academics/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DepartmentViewSet, 
    BatchViewSet, 
    SemesterViewSet, 
    ClassViewSet
)

# DRF Router setup
router = DefaultRouter()
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'batches', BatchViewSet, basename='batch')
router.register(r'semesters', SemesterViewSet, basename='semester')
router.register(r'classes', ClassViewSet, basename='class')

urlpatterns = [
    path('', include(router.urls)),
]