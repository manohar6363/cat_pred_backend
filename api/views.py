from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User

from .serializers import UserRegisterSerializer, UserLoginSerializer, DogImageSerializer
from .models import DogImage
from .manohar import predict_breed


# ----------- Auth Views -----------

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                "token": str(refresh.access_token),
                "refresh": str(refresh),
                "username": user.username,
                "email": user.email,
            }, status=status.HTTP_201_CREATED)

        print("Serializer errors:", serializer.errors)  # <--- Add this
        print("Data received:", request.data)          # <--- Add this
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username_or_email = serializer.validated_data["username"]
            password = serializer.validated_data["password"]

            # Try login with username or email
            user = authenticate(username=username_or_email, password=password)
            if not user:
                try:
                    user_obj = User.objects.get(email=username_or_email)
                    user = authenticate(username=user_obj.username, password=password)
                except User.DoesNotExist:
                    pass

            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    "token": str(refresh.access_token),
                    "refresh": str(refresh),
                    "username": user.username,
                    "email": user.email,
                }, status=status.HTTP_200_OK)

            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ----------- Dog Prediction View -----------

class DogBreedPredictView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = DogImageSerializer(data=request.data)
        if serializer.is_valid():
            dog_image = serializer.save(user=request.user)

            # Run prediction using manohar.py
            img_path = dog_image.image.path
            predictions = predict_breed(img_path)

            # Save top prediction
            if predictions:
                dog_image.predicted_breed = predictions[0]["breed"]
                dog_image.save()

            return Response({
                "message": "Prediction successful",
                "predictions": predictions
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)