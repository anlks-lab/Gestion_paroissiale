from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GroupeViewSet

router = DefaultRouter()
router.register("", GroupeViewSet, basename="groupes")

urlpatterns = [
    path("", include(router.urls)),
]
