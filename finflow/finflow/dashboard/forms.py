from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['title', 'amount', 'type', 'category', 'date', 'notes']
    
    def clean(self):
        cleaned_data = super().clean()
        transaction_type = cleaned_data.get('type')
        category = cleaned_data.get('category')
        
        if transaction_type == Transaction.EXPENSE and category in dict(Transaction.INCOME_CATEGORY_CHOICES).keys():
            raise forms.ValidationError("Expense transactions cannot have income categories.")
        
        if transaction_type == Transaction.INCOME and category in dict(Transaction.EXPENSE_CATEGORY_CHOICES).keys():
            raise forms.ValidationError("Income transactions cannot have expense categories.")
        
        return cleaned_data