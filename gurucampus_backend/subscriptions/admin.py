# subscriptions/admin.py
from django.contrib import admin
from .models import SubscriptionPlan, TenantSubscription

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    """
    Admin view for managing the SaaS product tiers (e.g., Basic, Standard).
    """
    list_display = ('name', 'price_per_month')

@admin.register(TenantSubscription)
class TenantSubscriptionAdmin(admin.ModelAdmin):
    """
    Admin view for managing a tenant's active subscription.
    """
    list_display = ('tenant', 'plan', 'start_date', 'end_date', 'is_active')
    list_filter = ('plan', 'is_active')
    search_fields = ('tenant__name',)
    
    # Allow the admin to quickly activate/deactivate a subscription
    list_editable = ('is_active', 'end_date')