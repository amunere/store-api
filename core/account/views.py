from django.db.models import Q
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import generics
from .models import User
from .serializers import (UserSerializer, 
                          RegisterSerializer)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class RegisterView(generics.CreateAPIView):
    """
    API endpoint for registration user
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer