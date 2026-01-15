from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import AccountsViewSet

router = DefaultRouter()
# Assuming AccountsViewSet is imported from views
router.register(r'avatars', AccountsViewSet, basename='avatar')

urlpatterns = [
    path('', include(router.urls)),
]