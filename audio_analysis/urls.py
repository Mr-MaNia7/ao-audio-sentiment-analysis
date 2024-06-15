from django.urls import include, path
from .views import AudioAnalysisViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'audios', AudioAnalysisViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
