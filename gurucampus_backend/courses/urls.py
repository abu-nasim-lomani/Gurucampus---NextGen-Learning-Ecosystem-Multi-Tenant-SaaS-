# courses/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet

# DRF-এর রাউটার স্বয়ংক্রিয়ভাবে CRUD (Create, Read, Update, Delete) URL তৈরি করে
router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')

urlpatterns = [
    path('', include(router.urls)),
]