from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TransactionViewSet, MembreDonsView

router = DefaultRouter()
router.register("transactions", TransactionViewSet, basename="transactions")

urlpatterns = [
    path("", include(router.urls)),
    path("rapport/", TransactionViewSet.as_view({"get": "rapport"}), name="rapport_financier"),
    path("membre/<int:pk>/dons/", MembreDonsView.as_view({"get": "retrieve"}), name="membre_dons"),
]
