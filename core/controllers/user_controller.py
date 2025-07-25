from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from core.services.user_service import UserService


class MeView(APIView):
    """
    View to retrieve the current user's information.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Handle GET requests to retrieve the current user's information.
        """
        service = UserService()
        data = service.get_user_details(request.user.id)
        return Response(data, status=status.HTTP_200_OK)