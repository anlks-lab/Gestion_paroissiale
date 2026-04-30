from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet, VenteViewSet

router = DefaultRouter()
router.register("articles", ArticleViewSet, basename="articles")
router.register("ventes", VenteViewSet, basename="ventes")

urlpatterns = [
    path("", include(router.urls)),
    path("alertes/", ArticleViewSet.as_view({"get": "alertes"}), name="alertes_stock"),
]
