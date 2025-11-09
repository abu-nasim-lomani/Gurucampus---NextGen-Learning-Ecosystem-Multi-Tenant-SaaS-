# marketplace/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    InstructorApplicationViewSet, 
    InstructorProfileViewSet, 
    OrderViewSet
)

# DRF Router setup
router = DefaultRouter()
router.register(r'instructor-applications', InstructorApplicationViewSet, basename='instructorapplication')
router.register(r'instructor-profiles', InstructorProfileViewSet, basename='instructorprofile')
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
]