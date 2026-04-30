from django.db.models import Sum, Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from core.permissions import IsAdmin, IsTreasurerOrAbove
from accounts.core.response import standardized_response
from .models import Transaction
from .serializers import TransactionSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.select_related("membre", "enregistre_par").all()
    serializer_class = TransactionSerializer

    def get_permissions(self):
        if self.action == "destroy":
            return [IsAdmin()]
        return [IsTreasurerOrAbove()]

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        serializer = self.get_serializer(qs, many=True)
        return Response(standardized_response(data=serializer.data))

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(standardized_response(data=serializer.data))

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(enregistre_par=request.user)
        return Response(
            standardized_response(data=serializer.data, message="Transaction enregistrée"),
            status=status.HTTP_201_CREATED,
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(standardized_response(message="Transaction supprimée"), status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["get"], permission_classes=[IsTreasurerOrAbove])
    def rapport(self, request):
        date_debut = request.query_params.get("date_debut")
        date_fin = request.query_params.get("date_fin")

        qs = self.get_queryset()
        if date_debut:
            qs = qs.filter(date__gte=date_debut)
        if date_fin:
            qs = qs.filter(date__lte=date_fin)

        totaux = qs.aggregate(
            total_recettes=Sum("montant", filter=Q(type="recette")),
            total_depenses=Sum("montant", filter=Q(type="depense")),
        )
        solde = (totaux["total_recettes"] or 0) - (totaux["total_depenses"] or 0)

        data = {
            "periode": {"debut": date_debut, "fin": date_fin},
            "total_recettes": totaux["total_recettes"] or 0,
            "total_depenses": totaux["total_depenses"] or 0,
            "solde": solde,
            "transactions": TransactionSerializer(qs, many=True).data,
        }
        return Response(standardized_response(data=data))


class MembreDonsView(viewsets.ViewSet):
    permission_classes = [IsTreasurerOrAbove]

    def retrieve(self, request, pk=None):
        from membres.models import Membre
        try:
            membre = Membre.objects.get(pk=pk)
        except Membre.DoesNotExist:
            return Response(
                standardized_response(success=False, error="Membre introuvable"),
                status=status.HTTP_404_NOT_FOUND,
            )
        dons = Transaction.objects.filter(membre=membre, categorie="don")
        serializer = TransactionSerializer(dons, many=True)
        total = dons.aggregate(total=Sum("montant"))["total"] or 0
        return Response(standardized_response(data={"membre": str(membre), "total_dons": total, "dons": serializer.data}))
