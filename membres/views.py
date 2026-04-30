from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.permissions import IsAdmin, IsSecretaryOrAbove
from accounts.core.response import standardized_response
from .models import Membre, Sacrement
from .serializers import MembreSerializer, MembreDetailSerializer, SacrementSerializer


class MembreViewSet(viewsets.ModelViewSet):
    queryset = Membre.objects.select_related("groupe", "user").all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return MembreDetailSerializer
        return MembreSerializer

    def get_permissions(self):
        if self.action == "destroy":
            return [IsAdmin()]
        if self.action in ("list", "retrieve"):
            return [IsSecretaryOrAbove()]
        return [IsSecretaryOrAbove()]

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
        serializer.save()
        return Response(
            standardized_response(data=serializer.data, message="Membre créé avec succès"),
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(standardized_response(data=serializer.data, message="Membre modifié"))

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(standardized_response(message="Membre supprimé"), status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["get"], permission_classes=[IsSecretaryOrAbove])
    def sacrements(self, request, pk=None):
        membre = self.get_object()
        sacrements = membre.sacrements.all()
        serializer = SacrementSerializer(sacrements, many=True)
        return Response(standardized_response(data=serializer.data))

    @action(detail=True, methods=["post"], permission_classes=[IsSecretaryOrAbove])
    def ajouter_sacrement(self, request, pk=None):
        membre = self.get_object()
        serializer = SacrementSerializer(data={**request.data, "membre": membre.id})
        serializer.is_valid(raise_exception=True)
        serializer.save(membre=membre)
        return Response(
            standardized_response(data=serializer.data, message="Sacrement enregistré"),
            status=status.HTTP_201_CREATED,
        )
