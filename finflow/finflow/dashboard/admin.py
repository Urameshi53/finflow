from django.contrib import admin
from .models import Transaction, Category

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('title', 'amount', 'type', 'category', 'date', 'created_at')
    list_filter = ('type', 'category', 'date')
    search_fields = ('title', 'notes')
    ordering = ('-date',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_custom')
    list_filter = ('is_custom',)
    search_fields = ('name',)
    ordering = ('name',)