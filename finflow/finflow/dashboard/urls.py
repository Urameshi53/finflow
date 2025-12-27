# urls.py (app-level)
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TransactionViewSet

router = DefaultRouter()
router.register(r'transactions', TransactionViewSet, basename='transaction')

# Add this if you want to disable the browsable API
# router = DefaultRouter(trailing_slash=False)

urlpatterns = [
    path('', include(router.urls)),
]