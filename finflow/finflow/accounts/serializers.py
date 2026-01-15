from rest_framework import serializers
from .models import Avatar
from django.contrib.auth.models import User 

class AvatarSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Avatar
        fields = ['id', 'user', 'currency']
        read_only_fields = ['id']