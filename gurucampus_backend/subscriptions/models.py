# subscriptions/models.py
from django.db import models
from tenants.models import Organization

class SubscriptionPlan(models.Model):
    """
    Defines the B2B SaaS Tiers (e.g., Free, Basic, Standard).
    This is managed by the Super Admin.
    """
    name = models.CharField(max_length=100) # e.g., "Basic Plan"
    price_per_month = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # We can link this to the `user_limit` later
    # For now, this just tracks the product.
    
    def __str__(self):
        return f"{self.name} (${self.price_per_month}/mo)"

class TenantSubscription(models.Model):
    """
    Links an Organization (Tenant) to their active plan.
    This tracks the B2B payment status.
    """
    tenant = models.OneToOneField(
        Organization, 
        on_delete=models.CASCADE, 
        related_name="subscription"
    )
    plan = models.ForeignKey(
        SubscriptionPlan, 
        on_delete=models.SET_NULL, # If plan is deleted, keep tenant
        null=True,
        related_name="tenants"
    )
    
    start_date = models.DateField()
    end_date = models.DateField(
        help_text="The date when the subscription expires."
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Is the subscription currently paid and active?"
    )

    def __str__(self):
        return f"{self.tenant.name}'s {self.plan.name} Plan"