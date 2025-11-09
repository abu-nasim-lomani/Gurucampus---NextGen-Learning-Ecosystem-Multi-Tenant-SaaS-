# subscriptions/views.py
from rest_framework import viewsets, permissions
from .models import SubscriptionPlan, TenantSubscription
from .serializers import SubscriptionPlanSerializer, TenantSubscriptionSerializer
from django_tenants.utils import schema_context # For security

class SubscriptionPlanViewSet(viewsets.ModelViewSet):
    """
    API endpoint for the B2B SaaS Tiers (Products).
    Only Super Admins can manage this.
    """
    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer
    # Only staff (Super Admins) can see or edit plans
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        # Plans must be created in the 'public' schema
        with schema_context('public'):
            serializer.save()

    def perform_update(self, serializer):
        # Plans must be updated in the 'public' schema
        with schema_context('public'):
            serializer.save()

    def perform_destroy(self, instance):
        # Plans must be deleted from the 'public' schema
        with schema_context('public'):
            instance.delete()

class TenantSubscriptionViewSet(viewsets.ModelViewSet):
    """
    API endpoint for a Tenant's active subscription.
    Only Super Admins can manage this.
    """
    queryset = TenantSubscription.objects.all()
    serializer_class = TenantSubscriptionSerializer
    # Only staff (Super Admins) can see or edit subscriptions
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        # Subscriptions must be created in the 'public' schema
        with schema_context('public'):
            serializer.save()

    def perform_update(self, serializer):
        # Subscriptions must be updated in the 'public' schema
        with schema_context('public'):
            serializer.save()

    def perform_destroy(self, instance):
        # Subscriptions must be deleted from the 'public' schema
        with schema_context('public'):
            instance.delete()