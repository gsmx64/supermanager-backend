import os
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from rest_framework import serializers, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from api.models import UserProfile
from api.services.mail import MailService


class AuthService:
    def __init__(self) -> None:
        self.mail_service = MailService()

    @staticmethod
    def validate(cls, User, data) -> dict:
        action = cls.context.get('action')
        request = cls.context.get('request')
        if not action:
            raise serializers.ValidationError('Action is required in serializer context.')
        if action == 'register':
            if not all(
                [
                    data.get('username'),
                    data.get('email'),
                    data.get('password'),
                    data.get('repeat_password'),
                    data.get('first_name'),
                    data.get('last_name')
                ]
            ):
                raise serializers.ValidationError('All register fields are required.')
            if data['password'] != data['repeat_password']:
                raise serializers.ValidationError({'password': 'Passwords do not match.'})
            if User.objects.filter(username=data['username']).exists():
                raise serializers.ValidationError({'username': 'Username already exists.'})
            if User.objects.filter(email=data['email']).exists():
                raise serializers.ValidationError({'email': 'Email already exists.'})

        elif action in ['login']:
            if not all([data.get('username'), data.get('password')]):
                raise serializers.ValidationError('Username and password are required for login.')
            user = authenticate(username=data['username'], password=data['password'])
            if not user:
                raise AuthenticationFailed('Invalid credentials.')
            if not user.is_active:
                raise AuthenticationFailed('User is inactive. Hold on while we reactivate your account.')
            data['user'] = user

        elif action == 'change_password':
            user = request.user
            user_id_reset = data.get('id', None)

            if not user or not user.is_authenticated or not hasattr(user, 'id'):
                raise serializers.ValidationError({'error.message': 'Authenticated user is required.'})

            if not data.get('id'):
                raise serializers.ValidationError('Authenticated user id is required.')

            if str(user.id) != str(user_id_reset):
                raise serializers.ValidationError({'error.message': 'You can only change your own password.', 'status': status.HTTP_401_UNAUTHORIZED})

            if not all([data.get('current_password'), data.get('password'), data.get('repeat_password')]):
                raise serializers.ValidationError('All reset password fields are required.')
            if data['password'] != data['repeat_password']:
                raise serializers.ValidationError({'password': 'Passwords do not match.'})
            data['user'] = user
            
        elif action == 'admin_change_password':
            user = request.user
            user_id_reset = data.get('id', None)
            
            if not user or not user.is_authenticated or not hasattr(user, 'id'):
                raise serializers.ValidationError({'error.message': 'Authenticated user is required.'})
            
            if not data.get('id'):
                raise serializers.ValidationError('Authenticated user id is required.')

            if not user.is_staff:
                raise serializers.ValidationError({'error.message': 'Only admins can change user passwords.', 'status': status.HTTP_403_FORBIDDEN})

            if not all([data.get('password'), data.get('repeat_password')]):
                raise serializers.ValidationError('All reset password fields are required.')
            if not user or not user.is_authenticated:
                raise serializers.ValidationError({'error.message': 'Authenticated user is required.'})
            if data['password'] != data['repeat_password']:
                raise serializers.ValidationError({'password': 'Passwords do not match.'})
            data['user'] = user

        elif action == 'forgot_password':
            if not data.get('forgot_email'):
                raise serializers.ValidationError('Email is required for forgot password.')
            if not User.objects.filter(email=data['forgot_email']).exists():
                return None

        elif action == 'access_token':
            if not all([data.get('username'), data.get('password')]):
                raise serializers.ValidationError('Username and password are required for token generation.')
            user = authenticate(username=data['username'], password=data['password'])
            if not user:
                raise serializers.ValidationError('Invalid username or password.')
            if not user.is_active:
                raise AuthenticationFailed('User is inactive. Hold on while we reactivate your account.')

            user.password = data['password']
            data['user'] = user

        elif action == 'refresh_token':
            refresh_token = data.get('refresh')
            if not refresh_token:
                raise serializers.ValidationError('Refresh token is required.')
            data['refresh'] = refresh_token

        elif action == 'verify_token':
            token = data.get('token')
            if not token:
                raise AuthenticationFailed({'error.message': 'Token is required.', 'status': status.HTTP_401_UNAUTHORIZED})
            data['token'] = token
        else:
            raise serializers.ValidationError('Invalid action: {}'.format(action))

        return data

    @staticmethod
    def register(cls, UserSerializer, UserProfileSerializer) -> dict:
        validated_data = cls.validated_data
        user = User.objects.create_user(
            username = validated_data['username'],
            email = validated_data['email'],
            password = validated_data['password'],
            first_name = validated_data.get('first_name', ''),
            last_name = validated_data.get('last_name', ''),
            is_active = False
        )

        user_profile, created = UserProfile.objects.get_or_create(user=user)
        
        request = cls.context.get('request')
        if request and hasattr(request, 'FILES'):
            user_profile.avatar = request.FILES.get('avatar')
        else:
            user_profile.avatar = validated_data.get('avatar', None)

        user_profile.phone = validated_data.get('phone', '')
        user_profile.mobile = validated_data.get('mobile', '')
        user_profile.address = validated_data.get('address', '')
        user_profile.city = validated_data.get('city', '')
        user_profile.state = validated_data.get('state', '')
        user_profile.zip_code = validated_data.get('zip_code', '')
        user_profile.country = validated_data.get('country', '')
        user_profile.birth = validated_data.get('birth', None)
        user_profile.title = validated_data.get('title', '')
        user_profile.about = validated_data.get('about', '')
        user_profile.save()

        user_data = UserSerializer(user).data
        user_profile_data = UserProfileSerializer(user_profile).data
        merged_data = {**user_data, **user_profile_data}
        return merged_data

    @staticmethod
    def login(cls, UserSerializer) -> dict:
        validated_data = cls.validated_data
        username = validated_data.get('username')
        password = validated_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise AuthenticationFailed("Invalid credentials.")
        if not user.is_active:
            raise AuthenticationFailed("User is inactive. Hold on while we reactivate your account.")
        access_token = AccessToken.for_user(user)
        refresh_token = RefreshToken.for_user(user)
        user_data = UserSerializer(user).data
        return {
            'access': str(access_token),
            'refresh': str(refresh_token),
            'user': user_data,
            'exp': access_token.payload.get('exp', None)
        }

    @staticmethod
    def change_password(cls) -> dict:
        validated_data = cls.validated_data
        request = cls.context['request']
        user = request.user

        password = validated_data.get('password')
        user.set_password(password)
        user.save()
        return {'message': 'Password changed successfully.'}

    @staticmethod
    def admin_change_password(cls) -> dict:
        validated_data = cls.validated_data
        request = cls.context.get('request')
        user = request.user

        password = validated_data.get('password')
        user.set_password(password)
        user.save()
        return {'message': 'Password changed successfully by admin.'}

    @staticmethod
    def forgot_password(cls) -> dict:
        email = cls.validated_data['forgot_email']
        user = User.objects.get(email=email)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_url = (settings.EMAIL_PWRESET_URL).format(FRONTEND_URL=settings.FRONTEND_URL, uid=uid, token=token)

        if settings.EMAIL_ENABLED:
            cls.mail_service.send_mail(
                to_email=email,
                subject=settings.EMAIL_PWRESET_SUBJECT,
                body=(settings.EMAIL_PWRESET_MESSAGE).format(reset_url=reset_url),
            )

        if (
            os.environ.get('ENVIRONMENT') == 'development' or
            os.environ.get('ENVIRON') == 'development' or
            os.environ.get('ENVIRONMENT') == 'testing' or
            os.environ.get('ENVIRON') == 'testing'
        ):
            return  {"message": f"[DEVELOPMENT-ONLY] Password reset link for {email}: {reset_url}"}

        return {"email": email}

    @staticmethod
    def access_token(cls, AuthTokenObtainPairSerializer) -> dict:
        user = cls.validated_data['user']
        serializer_token = AuthTokenObtainPairSerializer(data={
            'username': user.username,
            'password': cls.validated_data.get('password')
        })
        if serializer_token.is_valid():
            return serializer_token.validated_data
        return {"error": "Invalid credentials."}

    @staticmethod
    def refresh_token(cls, AuthTokenRefreshSerializer) -> dict:
        refresh_token = cls.validated_data['refresh']
        serializer_token = AuthTokenRefreshSerializer(data={
            'refresh': refresh_token
        })
        if serializer_token.is_valid():
            return serializer_token.validated_data
        return {"error": "Invalid refresh token."}

    @staticmethod
    def verify_token(cls, AuthTokenVerifySerializer) -> bool:
        serializer_token = AuthTokenVerifySerializer(data={
            'token': cls.validated_data.get('token')
        })
        try:
            if serializer_token.is_valid():
                return True
            else:
                return False
        except Exception:
            return False
