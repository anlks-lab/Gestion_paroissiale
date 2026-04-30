from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MembreViewSet

router = DefaultRouter()
router.register("", MembreViewSet, basename="membres")

urlpatterns = [
    path("", include(router.urls)),
]
