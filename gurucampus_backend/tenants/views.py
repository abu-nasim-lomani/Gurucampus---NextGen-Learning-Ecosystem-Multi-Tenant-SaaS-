# tenants/views.py
from rest_framework import viewsets, permissions
from .models import Organization
from .serializers import OrganizationSerializer
from django_tenants.utils import schema_context

class OrganizationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows organizations (tenants) to be viewed or edited.
    Only admin users can access this.
    """
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAdminUser]

    # --- এই নতুন মেথডটি যোগ করুন ---
    def perform_update(self, serializer):
        """
        'public' স্কিমাতে স্যুইচ করুন, তারপর সেভ করুন।
        """
        with schema_context('public'):
            serializer.save()