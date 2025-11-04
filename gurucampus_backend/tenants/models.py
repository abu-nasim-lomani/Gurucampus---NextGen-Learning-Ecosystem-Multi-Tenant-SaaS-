# tenants/models.py
from django.db import models
from django_tenants.models import TenantMixin, DomainMixin

class Organization(TenantMixin):
    """
    Represents a B2C or B2B Organization (Tenant).
    """
    name = models.CharField(max_length=255)
    
    # As per Architecture Guide (A.2 - Feature 4)
    user_limit = models.PositiveIntegerField(default=100) 
    
    # 'schema_name' is required by TenantMixin
    # We'll use auto_create_schema=True to automatically create schemas
    auto_create_schema = True

    def __str__(self):
        return self.name

class Domain(DomainMixin):
    """
    Represents the domain/subdomain for an Organization.
    """
    # 'tenant' (ForeignKey to Organization) is required by DomainMixin
    # 'domain' (CharField) is also required
    pass