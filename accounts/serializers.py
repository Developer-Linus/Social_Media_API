from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from .models import Profile



class CustomUserSerializer(serializers.ModelSerializer):
    # Make password write only to prevent it from being returned in response
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    # Meta data for the serializer
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'password']
    # Define custom create method for user creation
    def create(self, validated_data):
        # Create new user using validated data
        user = get_user_model().objects.create_user(
            username = validated_data['username'],
            email = validated_data['email'],
            password = validated_data['password']
        )
        # Generate new token for the user
        Token.objects.create(user=user)
        
        return user

# Login Serializer
class LoginSerializer(serializers.Serializer):
    # Define the email field
    email = serializers.EmailField()
    # Define the password and make it write only
    password = serializers.CharField(max_length=255, write_only=True)
    
    # Define validate method for checking email and password
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        
        # Check the provision of both email and password
        if email and password:
            # Find user with the provided email
            user = get_user_model().objects.filter(email=email).first()
            # Check if the user exists and the password is correct
            if user and user.check_password(password):
                # If credentials are correct, return user
                return {'user': user}
            else:
                # for invalid credentials, raise validation error
                raise serializers.ValidationError('Invalid email or password.')
        else:
            # If either email or password is missing, raise validation error
            raise serializers.ValidationError('Both email and password are required.')

# Token Serializer
class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ['key']
#Profile Serializer
class ProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    
    class Meta:
        model = Profile
        fields = ['user', 'address', 'phone_number']

class FollowSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()

    def validate_user_id(self, value):
        try:
            return get_user_model().objects.get(id=value)
        except get_user_model().DoesNotExist:
            raise serializers.ValidationError('User not found')

class UnfollowSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()

    def validate_user_id(self, value):
        try:
            return get_user_model().objects.get(id=value)
        except get_user_model().DoesNotExist:
            raise serializers.ValidationError('User not found')               
            