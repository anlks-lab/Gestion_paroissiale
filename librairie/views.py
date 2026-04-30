from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.permissions import IsAdmin, IsSecretaryOrAbove
from accounts.core.response import standardized_response
from .models import Article, Vente
from .serializers import ArticleSerializer, VenteSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get_permissions(self):
        if self.action == "destroy":
            return [IsAdmin()]
        if self.action in ("list", "retrieve", "alertes"):
            return [IsAuthenticated()]
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
            standardized_response(data=serializer.data, message="Article ajouté"),
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(standardized_response(data=serializer.data, message="Article modifié"))

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(standardized_response(message="Article supprimé"), status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["get"], permission_classes=[IsSecretaryOrAbove])
    def alertes(self, request):
        articles_alerte = [a for a in self.get_queryset() if a.en_alerte]
        serializer = self.get_serializer(articles_alerte, many=True)
        return Response(standardized_response(data=serializer.data))


class VenteViewSet(viewsets.ModelViewSet):
    queryset = Vente.objects.select_related("article", "membre", "enregistre_par").all()
    serializer_class = VenteSerializer
    http_method_names = ["get", "post", "head", "options"]
    permission_classes = [IsSecretaryOrAbove]

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        serializer = self.get_serializer(qs, many=True)
        return Response(standardized_response(data=serializer.data))

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(enregistre_par=request.user)
        return Response(
            standardized_response(data=serializer.data, message="Vente enregistrée"),
            status=status.HTTP_201_CREATED,
        )
