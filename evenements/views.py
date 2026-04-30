from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.permissions import IsAdmin, IsSecretaryOrAbove
from accounts.core.response import standardized_response
from .models import Evenement, Participation
from .serializers import EvenementSerializer, ParticipationSerializer


class EvenementViewSet(viewsets.ModelViewSet):
    queryset = Evenement.objects.select_related("createur").prefetch_related("participations").all()
    serializer_class = EvenementSerializer

    def get_permissions(self):
        if self.action == "destroy":
            return [IsAdmin()]
        if self.action in ("create", "update", "partial_update", "inscrire"):
            return [IsSecretaryOrAbove()]
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
        serializer.save(createur=request.user)
        return Response(
            standardized_response(data=serializer.data, message="Événement créé"),
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(standardized_response(data=serializer.data, message="Événement modifié"))

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(standardized_response(message="Événement supprimé"), status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["post"], permission_classes=[IsSecretaryOrAbove])
    def inscrire(self, request, pk=None):
        evenement = self.get_object()
        membre_id = request.data.get("membre")
        if not membre_id:
            return Response(
                standardized_response(success=False, error="Champ 'membre' requis"),
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = ParticipationSerializer(
            data={"evenement": evenement.id, "membre": membre_id}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            standardized_response(data=serializer.data, message="Membre inscrit"),
            status=status.HTTP_201_CREATED,
        )

    @action(detail=True, methods=["get"], permission_classes=[IsSecretaryOrAbove])
    def participants(self, request, pk=None):
        evenement = self.get_object()
        participations = evenement.participations.select_related("membre").all()
        serializer = ParticipationSerializer(participations, many=True)
        return Response(standardized_response(data=serializer.data))
