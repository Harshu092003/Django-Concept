from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.serializers import ProfileSerializer
from myapp.models import Profile


@api_view(["GET"])
def get_method(requests):
    profile = Profile.objects.all()
    serializer = ProfileSerializer(profile, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def post_method(requests):
    serializer = ProfileSerializer(data=requests.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(["PUT"])
def put_method(requests, pk):
    profile = Profile.objects.get(pk=pk)
    serializer = ProfileSerializer(profile, data=requests.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(["DELETE"])
def delete_method(requests, pk):
    profile = Profile.objects.filter(pk=pk)
    if profile.exists():
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(
        {"error": f"profile does not exist with id: {pk}"},
        status=status.HTTP_404_NOT_FOUND,
    )


from rest_framework import generics

from .serializers import RegisterSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer


from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import LoginSerializer


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)

        return Response({"refresh": str(refresh), "access": str(refresh.access_token)})


from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import PasswordResetRequestSerializer


class PasswordResetRequestView(APIView):
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        user = User.objects.filter(email=email).first()

        if user:
            token = PasswordResetTokenGenerator().make_token(user)
            return Response(
                {
                    "message": "Password reset token generated",
                    "token": token,
                    "user_id": user.id,
                }
            )

        return Response({"error": "User not found"}, status=404)


from django.contrib.auth.tokens import PasswordResetTokenGenerator

from .serializers import PasswordResetConfirmSerializer


class PasswordResetConfirmView(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")
        token = request.data.get("token")

        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.get(id=user_id)

        if PasswordResetTokenGenerator().check_token(user, token):
            user.set_password(serializer.validated_data["new_password"])
            user.save()
            return Response({"message": "Password reset successful"})

        return Response({"error": "Invalid token"}, status=400)
