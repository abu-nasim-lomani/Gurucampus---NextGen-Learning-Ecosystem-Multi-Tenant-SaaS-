# users/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegistrationViewSet

# DRF Router setup
router = DefaultRouter()
router.register(r'register', RegistrationViewSet, basename='register')

urlpatterns = [
    path('', include(router.urls)),
]