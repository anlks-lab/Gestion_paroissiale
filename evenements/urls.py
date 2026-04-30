from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EvenementViewSet

router = DefaultRouter()
router.register("", EvenementViewSet, basename="evenements")

urlpatterns = [
    path("", include(router.urls)),
]
