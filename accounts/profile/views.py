import logging
import traceback

from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import status

from accounts.core.base_view import BaseAPIView
from .services import ProfileService
from ..core.response import standardized_response

logger = logging.getLogger(__name__)


class UserProfileView(BaseAPIView):
    """API endpoint for user profile operations"""

    permission_classes = [AllowAny]
    throttle_classes = [UserRateThrottle]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get(self, request):
        """get User profile data"""
        try:
            # use service layer to get user profile data
            user_data = ProfileService.get_profile(request.user)
            return Response(standardized_response(success=True, data=user_data))
        except Exception as e:
            logger.error(f"Profile fetch error: {str(e)}")
            logger.error(traceback.format_exc())
            return Response(
                standardized_response(
                    success=False, error="Failed to retrieve profile"
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def put(self, request):
        """Update full user profile"""
        try:
            # Log incoming request for debugging
            logger.info(f"Profile update request - Data key: {request.data.keys()}")
            logger.info(
                f"Profile update request - Files key: {list(request.FILES.keys()) if request.FILES else 'No files'}"
            )

            # use service layer for profile update logic
            success, response_data, status_code = ProfileService.update_profile(
                user=request.user, data=request.data, files=request.FILES
            )

            return Response(standardized_response(**response_data), status=status_code)
        except Exception as e:
            logger.error(f"Profile update error: {str(e)}")
            logger.error(traceback.format_exc())
            return Response(
                standardized_response(success=False, error="Profile update failed"),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def patch(self, request):
        """Partial user profile update"""
        try:
            # Log incoming request for debugging
            logger.info(f"Profile patch request - Data keys: {list(request.data.keys)}")
            logger.info(
                f"Profile patch request - Files keys: {list(request.FILES.keys) if request.FILES else 'No files'}"
            )

            # Use service layer for partial profile update
            success, response_data, status_code = ProfileService.update_profile(
                user=request.user, data=request.data, files=request.FILES
            )
            return Response(standardized_response(**response_data), status=status_code)
        except Exception as e:
            logger.error(f"Profile patch error: {str(e)}")
            logger.error(traceback.format_exc())
            return Response(
                standardized_response(success=False, error="Profile update failed"),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
