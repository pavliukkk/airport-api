from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.serializers import UserSerializer


@extend_schema(
    tags=["User"],
    summary="Create a new user",
    description="Creates a new user account.",
    request=UserSerializer,
    responses={
        201: UserSerializer,
    },
)
class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = ()


@extend_schema(
    tags=["User"],
    summary="Get or update current user",
    description=(
        "Returns information about the currently authenticated user "
        "or updates their profile."
    ),
    request=UserSerializer,
    responses={
        200: UserSerializer,
        401: {
            "description": "Authentication credentials were not provided "
            "or are invalid."
        },
    },
)
class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user
