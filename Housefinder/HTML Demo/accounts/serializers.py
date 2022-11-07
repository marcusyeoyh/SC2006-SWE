from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from .models import Favourite
from djoser.serializers import UserCreateSerializer

class UserCreateSerializer(UserCreateSerializer):
    class Meta:
        User = get_user_model()
        model = User
        fields = ('email', 'first_name', 'last_name', 'is_superuser', 'password')


class FavouriteSerializer(ModelSerializer):
    email = serializers.EmailField(source="user.email")
    class Meta:
        model = Favourite
        fields = ('email', 'block', 'street_name', 'predictedprice', 'flat_type')
        


class UserSerializer(ModelSerializer):
    class Meta:
        User = get_user_model()
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    """
    This serializer defines two fields for authentication:
    * email
    * password
    It will try to authenticate the user when validated.
    """

    email = serializers.CharField(
        label="email",
        write_only=True
    )

    password = serializers.CharField(
        label="password",
        # This will be used when DRF browsable API is enabled
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        # Take email and password from request
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            # Attempt to authenticate the user using basic Django auth framework
            user = authenticate(
                request=self.context.get('request'),
                email=email,
                password=password
            )

            if not user:
                # If user not found, raise a validation error
                msg = 'Access denied: wrong email or password or both'
                raise serializers.ValidationError(msg, code='authorization')

        else:
            msg = 'Both "email" and "password" are required'
            raise serializers.ValidationError(msg, code='authorization')
        
        # We have a valid user, put it in the serializer's validated_data
        # It will be used in the view
        attrs['user'] = user
        return attrs