from requests import Response
from rest_framework import serializers
from .models import Transaction, Category
from rest_framework import permissions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from http import HTTPStatus as status
from accounts.models import Avatar

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # 👇 attach user data here
        data["user"] = {
            "id": self.user.id,
            "username": self.user.username,
            "email": self.user.email,
            "is_staff": self.user.is_staff,
            "color": getattr(getattr(self.user, "avatar", None), "color", None),
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

    
    # CREATE
    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # UPDATE
    def put(self, request, pk):
        transaction = Transaction.objects.get(pk=pk)
        serializer = TransactionSerializer(transaction, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # DELETE
    def delete(self, request, pk):
        transaction = Transaction.objects.get(pk=pk)
        transaction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    
class CategorySerializer(serializers.ModelSerializer):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    class Meta:
        model = Category
        fields = ['id', 'name', 'is_custom', 'icon', 'color']