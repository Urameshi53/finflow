from rest_framework import serializers
from .models import Avatar
from django.contrib.auth.models import User 
from requests import Response
from http import HTTPStatus as status

class AvatarSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Avatar
        fields = ['id', 'user', 'currency']
        read_only_fields = ['id']
        
    def put(self, request, pk):
        avatar = Avatar.objects.get(pk=pk)
        serializer = AvatarSerializer(avatar, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)