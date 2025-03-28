from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from.serializers import CustomUserSerializer, LoginSerializer, TokenSerializer, ProfileSerializer, FollowSerializer, UnfollowSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from .models import Profile
from rest_framework import permissions

CustomUser = get_user_model()

# view for registration endpoint
class RegisterView(APIView):
    # Define POST method for user registration
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Generate token
            token = Token.objects.get(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# Login view for login endpoint
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            # Get or create token for the user
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token':token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# View for token endpoint
class TokenView(APIView):
    def get(self, request, pk):
        try:
            user = CustomUser.objects.get(pk=pk)
            token = Token.objects.get(user=user)
            serializer = TokenSerializer(token)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Token.DoesNotExist:
            return Response({'error': 'Token not found'}, status=status.HTTP_404_NOT_FOUND)
# Profile View
class ProfileView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def get(self, request, pk):
        try:
            user = CustomUser.objects.get(pk=pk)
            profile = request.user.profile
            serializer = ProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found!'}, status=status.HTTP_404_NOT_FOUND)
        except Profile.DoesNotExist:
            return Response({'error': 'Profile not found.'}, status=status.HTTP_404_NOT_FOUND)

# Define a view for following users
class FollowView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FollowSerializer

    def get(self, request):
        # Get all users
        users = CustomUser.objects.all()
        # Create a serializer to serialize the users
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # Get the serializer instance
        serializer = self.get_serializer(data=request.data)
        # Validate the data
        serializer.is_valid(raise_exception=True)
        # Get the user to follow
        user_to_follow = serializer.validated_data['user_id']
        # Get the current user
        current_user = request.user
        
        # Check if the user is already following the user to follow
        if user_to_follow in current_user.following.all():
            return Response({'error': 'You are already following this user.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Add the user to follow to the current user's following list
        current_user.following.add(user_to_follow)
        return Response({'message': 'You are now following this user.'}, status=status.HTTP_201_CREATED)

# Define a view for unfollowing users
class UnfollowView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UnfollowSerializer

    def get(self, request):
        # Get all users
        users = CustomUser.objects.all()
        # Create a serializer to serialize the users
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # Get the serializer instance
        serializer = self.get_serializer(data=request.data)
        # Validate the data
        serializer.is_valid(raise_exception=True)
        # Get the user to unfollow
        user_to_unfollow = serializer.validated_data['user_id']
        # Get the current user
        current_user = request.user
        
        # Check if the user is not following the user to unfollow
        if user_to_unfollow not in current_user.following.all():
            return Response({'error': 'You are not following this user'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Remove the user to unfollow from the current user's following list
        current_user.following.remove(user_to_unfollow)
        return Response({'message': 'You have successfully unfollowed this user.'}, status=status.HTTP_200_OK)