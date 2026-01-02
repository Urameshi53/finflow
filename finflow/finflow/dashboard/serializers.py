from rest_framework import serializers
from .models import Transaction, Category
from rest_framework import permissions


class TransactionSerializer(serializers.ModelSerializer):
    # Format the date for frontend
    date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    class Meta:
        model = Transaction
        fields = ['id', 'title', 'amount', 'type', 'category', 'date', 'notes', 'created_at', 'updated_at']
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