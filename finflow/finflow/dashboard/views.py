from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Transaction, Category
from .serializers import TransactionSerializer, CategorySerializer
from django.db.models import Sum
from datetime import datetime, timedelta
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'category']
    search_fields = ['title', 'notes']
    ordering_fields = ['date', 'amount', 'created_at']
    permission_classes = [permissions.IsAuthenticated] # API Authentication
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by date range if provided
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if start_date and end_date:
            queryset = queryset.filter(date__range=[start_date, end_date])
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get summary statistics"""
        queryset = self.filter_queryset(self.get_queryset())
        
        total_income = queryset.filter(type=Transaction.INCOME).aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        total_expense = queryset.filter(type=Transaction.EXPENSE).aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        balance = total_income - total_expense
        
        # Category breakdown
        expense_by_category = queryset.filter(type=Transaction.EXPENSE).values(
            'category'
        ).annotate(total=Sum('amount')).order_by('-total')
        
        income_by_category = queryset.filter(type=Transaction.INCOME).values(
            'category'
        ).annotate(total=Sum('amount')).order_by('-total')
        
        return Response({
            'total_income': float(total_income),
            'total_expense': float(total_expense),
            'balance': float(balance),
            'expense_by_category': list(expense_by_category),
            'income_by_category': list(income_by_category),
        })
    
    @action(detail=False, methods=['get'])
    def categories(self, request):
        """Get all available categories"""
        return Response({
            'expense_categories': Transaction.EXPENSE_CATEGORY_CHOICES,
            'income_categories': Transaction.INCOME_CATEGORY_CHOICES,
        })
    
    
@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    
    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    else:
        return Response({'error': 'Invalid credentials'}, status=400)
    

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]