# subscriptions/serializers.py
from rest_framework import serializers
from .models import SubscriptionPlan, TenantSubscription

class SubscriptionPlanSerializer(serializers.ModelSerializer):
    """
    Serializer for the B2B SaaS Tiers (Products).
    """
    class Meta:
        model = SubscriptionPlan
        fields = ['id', 'name', 'price_per_month']

class TenantSubscriptionSerializer(serializers.ModelSerializer):
    """
    Serializer for a Tenant's active subscription.
    """
    plan = SubscriptionPlanSerializer(read_only=True)
    plan_id = serializers.PrimaryKeyRelatedField(
        queryset=SubscriptionPlan.objects.all(),
        source='plan',
        write_only=True
    )
    
    class Meta:
        model = TenantSubscription
        fields = [
            'id', 
            'tenant', 
            'plan', # Read-only (nested details)
            'plan_id', # Write-only (for updates)
            'start_date', 
            'end_date', 
            'is_active'
        ]