import logging
import traceback

from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from .response import *

logger = logging.getLogger(__name__)


class BaseAPIView(APIView):
    """
    Vue de base pour les autres vues.
    Fournit des fonctionnalités communes telles que la gestion des erreurs.
    """

    def handle_exception(self, exc):
        if isinstance(exc, AuthenticationFailed):
            return Response(
                standardized_response(success=False, message=str(exc)),
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Log the exception with traceback
        logger.error(f"Exception in {self.__class__.__name__}: {str(exc)}")
        traceback_str = "".join(traceback.format_tb(exc.__traceback__))
        logger.error(f"Traceback: {traceback_str}")

        # Call the parent class's handle_exception method
        return super().handle_exception(exc)
