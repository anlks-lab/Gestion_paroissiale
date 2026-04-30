from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.permissions import IsAdmin, IsSecretaryOrAbove
from accounts.core.response import standardized_response
from .models import Groupe
from .serializers import GroupeSerializer


class GroupeViewSet(viewsets.ModelViewSet):
    queryset = Groupe.objects.select_related("responsable").all()
    serializer_class = GroupeSerializer

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [IsAuthenticated()]
        if self.action in ("create", "update", "partial_update", "destroy"):
            return [IsAdmin()]
        return [IsAuthenticated()]

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
            standardized_response(data=serializer.data, message="Groupe créé avec succès"),
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(standardized_response(data=serializer.data, message="Groupe modifié"))

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(standardized_response(message="Groupe supprimé"), status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["get"], permission_classes=[IsAuthenticated])
    def membres(self, request, pk=None):
        groupe = self.get_object()
        from membres.serializers import MembreSerializer
        membres = groupe.membres.all()
        serializer = MembreSerializer(membres, many=True)
        return Response(standardized_response(data=serializer.data))
