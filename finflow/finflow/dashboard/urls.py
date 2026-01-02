# urls.py (app-level)
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TransactionViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'transactions', TransactionViewSet, basename='transaction')
router.register(r'categories', CategoryViewSet, basename='category')
# Add this if you want to disable the browsable API
# router = DefaultRouter(trailing_slash=False)

urlpatterns = [
    path('', include(router.urls)),
]