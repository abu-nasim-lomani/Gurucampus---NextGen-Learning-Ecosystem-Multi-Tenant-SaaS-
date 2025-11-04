# tenants/views.py
from rest_framework import viewsets, permissions
from .models import Organization
from .serializers import OrganizationSerializer

class OrganizationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows organizations (tenants) to be viewed or edited.
    Only admin users can access this.
    """
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    
    # শুধুমাত্র অ্যাডমিনরাই নতুন টেন্যান্ট তৈরি বা দেখতে পারবেন।
    permission_classes = [permissions.IsAdminUser]