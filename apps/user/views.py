from rest_framework import status, permissions
from .serializers import *
from .models import *
from rest_framework.views import APIView
from .models import *
from core.response import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

class RegistrationView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CustomTokenObtainPairSerializer
    
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Generate tokens using context
            token_serializer = self.serializer_class(context={"user": user})
            token_data = token_serializer.validate({})

            response_data = {
                'access': token_data['access'],
                'refresh': token_data['refresh'],
            }

            return CustomApiResponse(
                status='success',
                message='Registration successful!',
                data=response_data,
                code=status.HTTP_201_CREATED
            ).get_response()

        return CustomApiResponse(
            status='error',
            message='Registration failed',
            data=serializer.errors,
            code=status.HTTP_400_BAD_REQUEST
        ).get_response()
    


class CustomTokenObtainPairView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        data = request.data
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return CustomApiResponse(
                status="error",
                message="Email and password are required.",
                data={},
                code=status.HTTP_400_BAD_REQUEST
            ).get_response()

        user = authenticate(request, email=email, password=password)

        if user is not None:
            serializer = CustomTokenObtainPairSerializer(context={"user": user})
            tokens = serializer.validate({})  # Empty dict, you're using context
            return CustomApiResponse(
                status="success",
                message="Login successful.",
                data={
                    "access": tokens["access"],
                    "refresh": tokens["refresh"]
                },
                code=status.HTTP_200_OK
            ).get_response()
        else:
            return CustomApiResponse(
                status="error",
                message="Invalid credentials.",
                data={},
                code=status.HTTP_401_UNAUTHORIZED
            ).get_response()
        


class CustomTokenRefreshView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = TokenRefreshSerializer(data=request.data)

        if serializer.is_valid():
            return CustomApiResponse(
                status='success',
                message='Access token refreshed successfully',
                data=serializer.validated_data,
                code=status.HTTP_200_OK
            ).get_response()

        return CustomApiResponse(
            status='error',
            message='Invalid refresh token',
            data=serializer.errors,
            code=status.HTTP_401_UNAUTHORIZED
        ).get_response()