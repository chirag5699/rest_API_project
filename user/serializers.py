from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
# from business.models import Business
from .models import User


class AuthUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'role'
        )


class AuthUserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('__all__')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        auth_user = User.objects.create_user(**validated_data)
        return auth_user


class AuthUserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128, write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    role = serializers.CharField(read_only=True)

    def create(self, validated_date):
        pass

    def update(self, instance, validated_data):
        pass

    def validate(self, data):
        email = data['email']
        password = data['password']
        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid login credentials")
        try:
            access = AccessToken.for_user(user)
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh)
            access_token = str(access)

            update_last_login(None, user)

            validation = {
                'access': access_token,
                'refresh': refresh_token,
                'email': user.email,
                'full_name': user.first_name + " " + user.last_name,
                'role': user.role,
            }
            return validation
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid login credentials")


class AuthUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}


class AuthUserDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


# class UserBusinessSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Business
#         fields = ['id', 'name', 'description', 'URL', 'logo']
