from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContributorViewSet, CustomUserViewSet

router = DefaultRouter()
router.register(r'users', CustomUserViewSet)
router.register(r'contributors', ContributorViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
