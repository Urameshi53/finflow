from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    is_custom = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    
    TYPE_CHOICES = [
        ('Expense', 'Expense'),
        ('Income', 'Income'),
    ]
    
    EXPENSE = 'Expense'
    INCOME = 'Income'
    
    EXPENSE_CATEGORY_CHOICES = [
        ('Food', 'Food'),
        ('Transport', 'Transport'),
        ('Utilities', 'Utilities'),
        ('Entertainment', 'Entertainment'),
        ('Healthcare', 'Healthcare'),
        ('Other', 'Other'),
    ]
    
    INCOME_CATEGORY_CHOICES = [
        ('Salary', 'Salary'),
        ('Business', 'Business'),
        ('Investment', 'Investment'),
        ('Gift', 'Gift'),
        ('Other', 'Other'),
    ]
    
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.amount} ({self.type})"