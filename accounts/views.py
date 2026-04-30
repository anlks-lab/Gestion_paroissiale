# # apps/accounts/views.py
from rest_framework import status, viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import UserSerializer



# class UserViewSet(viewsets.ReadOnlyModelViewSet):
#     """
#     Consultation des utilisateurs (admin ou membres de l'établissement)
#     """

#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticated]

    