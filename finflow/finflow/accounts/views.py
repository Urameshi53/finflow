from django.shortcuts import render
from rest_framework import viewsets, permissions

from .serializers import AvatarSerializer
from .models import Avatar

class AccountsViewSet(viewsets.ModelViewSet):
    queryset = Avatar.objects.all()
    serializer_class = AvatarSerializer
    permission_classes = [permissions.IsAuthenticated]  # API Authentication

    def get_queryset(self):
        return Avatar.objects.filter(user=self.request.user)
    