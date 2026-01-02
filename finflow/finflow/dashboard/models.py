from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator

class Transaction(models.Model):
    # Transaction Type Choices
    EXPENSE = 'Expense'
    INCOME = 'Income'
    TRANSACTION_TYPE_CHOICES = [
        (EXPENSE, 'Expense'),
        (INCOME, 'Income'),
    ]
    
    # Expense Category Choices
    FOOD = 'Food'
    TRANSPORT = 'Transport'
    TITHE = 'Tithe'
    UTILITIES = 'Utilities'
    SHOPPING = 'Shopping'
    SPOTIFY_EXPENSE = 'Spotify'
    HEALTHCARE = 'Healthcare'
    GROCERIES = 'Groceries'
    OTHER_EXPENSES = 'Other Expenses'
    
    EXPENSE_CATEGORY_CHOICES = [
        (FOOD, 'Food'),
        (TRANSPORT, 'Transport'),
        (TITHE, 'Tithe'),
        (UTILITIES, 'Utilities'),
        (SHOPPING, 'Shopping'),
        (SPOTIFY_EXPENSE, 'Spotify'),
        (HEALTHCARE, 'Healthcare'),
        (GROCERIES, 'Groceries'),
        (OTHER_EXPENSES, 'Other Expenses'),
    ]
    
    # Income Category Choices
    SALARY = 'Salary'
    FREELANCE = 'Freelance'
    INVESTMENT = 'Investment'
    GIFT = 'Gift'
    SPOTIFY_INCOME = 'Spotify-IN'
    OTHER_INCOME = 'Other Income'
    
    INCOME_CATEGORY_CHOICES = [
        (SALARY, 'Salary'),
        (FREELANCE, 'Freelance'),
        (INVESTMENT, 'Investment'),
        (GIFT, 'Gift'),
        (SPOTIFY_INCOME, 'Spotify-IN'),
        (OTHER_INCOME, 'Other Income'),
    ]
    
    # All categories combined for database storage
    ALL_CATEGORY_CHOICES = EXPENSE_CATEGORY_CHOICES + INCOME_CATEGORY_CHOICES
    
    title = models.CharField(max_length=200)
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    type = models.CharField(
        max_length=10,
        choices=TRANSACTION_TYPE_CHOICES
    )
    date = models.DateTimeField(default=timezone.now)
    
    # Category field - will store all categories
    category = models.CharField(
        max_length=50,
        choices=ALL_CATEGORY_CHOICES
    )
    
    notes = models.TextField(blank=True, null=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['type', 'date']),
            models.Index(fields=['category', 'date']),
        ]
    
    def __str__(self):
        return f"{self.title} - ${self.amount} ({self.type})"
    
    def save(self, *args, **kwargs):
        # You could add custom validation logic here if needed
        # For example, ensure expense categories are only used with expense type
        # and income categories with income type
        super().save(*args, **kwargs)
    
    def get_category_display_with_type(self):
        """Returns category display name with type context"""
        return dict(self.ALL_CATEGORY_CHOICES).get(self.category, self.category)
    
    @property
    def is_expense(self):
        return self.type == self.EXPENSE
    
    @property
    def is_income(self):
        return self.type == self.INCOME
    

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    TYPE_CHOICES = [
        ('Expense', 'Expense'),
        ('Income', 'Income'),
    ]

    type = models.CharField(max_length=10, unique=False, choices=TYPE_CHOICES)
    is_custom = models.BooleanField(default=False)

    def __str__(self):
        return self.name