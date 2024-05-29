from django.urls import include, path
from .views import AudioFileViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'audios', AudioFileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
