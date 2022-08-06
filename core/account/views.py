"""API classes"""
import logging
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer

# Create your views here.


logger = logging.getLogger("django")


class RegisterView(generics.GenericAPIView):
    """Register API"""

    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(operation_description="register")
    def post(self, request):
        """We are creating tokens"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "data": request.data,
                "is admin": user.is_superuser,
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
            }
        )


class LoginAPIView(generics.GenericAPIView):
    """Login API"""

    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(operation_description="login")
    def post(self, request):
        """login user"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)


##################################################################
register_api = RegisterView.as_view()
login_api = LoginAPIView.as_view()
