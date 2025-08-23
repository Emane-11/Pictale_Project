from rest_framework import generics, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

User = get_user_model()

# Serializer for user registration
class UserRegisterSerializer(ModelSerializer):
    password2 = serializers.CharField(write_only=True)  # confirmation field

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'password2')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords must match."})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')  # remove before creating user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


# Registration API
class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(id=response.data['id'])
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "message": "🎉 Account created successfully! Welcome to Pictale.",
            "user": response.data,
            "token": token.key
        }, status=status.HTTP_201_CREATED)



# Login API (returns token)
class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'user_id': token.user_id, 'username': token.user.username})


# Logout API
class LogoutAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()  # deletes the token
        return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)

''' Protected API view : For testing 

class ProtectedAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Only logged-in users can access

    def get(self, request):
        return Response(
            {"message": f"Hello {request.user.username}, you have access to this protected view!"},
            status=status.HTTP_200_OK
        )
'''

# Profile API view

from ..serializers import ProfileSerializer

class ProfileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):  # full update
        serializer = ProfileSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):  # partial update
        serializer = ProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

