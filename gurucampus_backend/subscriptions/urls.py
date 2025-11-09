# subscriptions/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubscriptionPlanViewSet, TenantSubscriptionViewSet

# DRF Router setup
router = DefaultRouter()
router.register(r'plans', SubscriptionPlanViewSet, basename='subscriptionplan')
router.register(r'tenant-subscriptions', TenantSubscriptionViewSet, basename='tenantsubscription')

urlpatterns = [
    path('', include(router.urls)),
]