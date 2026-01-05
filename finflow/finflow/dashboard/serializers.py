from rest_framework import serializers
from .models import Transaction, Category
from rest_framework import permissions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # 👇 attach user data here
        data["user"] = {
            "id": self.user.id,
            "username": self.user.username,
            "email": self.user.email,
            "is_staff": self.user.is_staff,
        }

        return data



class TransactionSerializer(serializers.ModelSerializer):
    # Format the date for frontend
    date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    class Meta:
        model = Transaction
        fields = ['id', 'user','title', 'amount', 'type', 'category', 'date', 'notes', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate(self, data):
        # Add your validation logic here
        if data.get('type') == Transaction.EXPENSE and data.get('amount') <= 0:
            raise serializers.ValidationError("Expense amount must be positive")
        return data
    
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'is_custom']