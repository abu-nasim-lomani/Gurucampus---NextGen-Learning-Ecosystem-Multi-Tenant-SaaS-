# users/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .serializers import RegistrationSerializer

class RegistrationViewSet(viewsets.ViewSet):
    """
    A public ViewSet for new user registration.
    """
    # This is the crucial part:
    # Allow any user (even unauthenticated) to access this endpoint.
    permission_classes = [permissions.AllowAny]

    def create(self, request):
        """
        Handle a POST request to register a new user.
        """
        serializer = RegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            
            # We don't return the password, just a success message
            response_data = {
                "message": "User registered successfully.",
                "email": user.email,
                "status": "Pending"
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            # Return validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)