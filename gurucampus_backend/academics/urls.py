# academics/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DepartmentViewSet, 
    BatchViewSet, 
    SemesterViewSet, 
    ClassViewSet,
    ClassroomMemberViewSet,
    ManageMemberView
)

# DRF Router setup
router = DefaultRouter()
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'batches', BatchViewSet, basename='batch')
router.register(r'semesters', SemesterViewSet, basename='semester')
router.register(r'classes', ClassViewSet, basename='class')
router.register(r'classroom-members', ClassroomMemberViewSet, basename='classroommember') 

urlpatterns = [
    path('', include(router.urls)),
    path(
        'classes/<int:class_pk>/manage-member/', 
        ManageMemberView.as_view(), 
        name='class-manage-member'
    ),
]