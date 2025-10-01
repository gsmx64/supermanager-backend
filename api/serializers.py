from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import serializers
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
    TokenVerifySerializer
)
from rest_framework.validators import UniqueTogetherValidator

from api.services.auth import AuthService
from api.models import (
    UserProfile, Locations, LocationZones, DeviceTypes, DeviceMarks,
    DeviceModels, DeviceSystems, DeviceBuilds, DeviceProcessors,
    DeviceRAMs, DeviceDisks, Softwares, DeviceSoftwares, Devices,
    NotificationTypes, Notifications, AppSettings, UserSettings
)
from api.filters import (
    LocationsFilter, LocationZonesFilter, DeviceTypesFilter,
    DeviceMarksFilter, DeviceModelsFilter, DeviceSystemsFilter,
    DeviceBuildsFilter, DeviceProcessorsFilter, DeviceRAMsFilter,
    DeviceDisksFilter, SoftwaresFilter, DevicesFilter,
    DeviceSoftwaresFilter, NotificationTypesFilter,
    NotificationsFilter
)
from api.pagination import DefaultLimitOffsetPagination


class AuthCustomSerializer(serializers.Serializer):
    """
    Serializer for custom authentication.
    """
    # Signup fields
    username = serializers.CharField(min_length=5, max_length=20, required=False)
    password = serializers.CharField(min_length=8, max_length=128, write_only=True, required=False)
    repeat_password = serializers.CharField(min_length=8, max_length=128, write_only=True, required=False)
    email = serializers.EmailField(min_length=8, max_length=120, required=False)
    first_name = serializers.CharField(min_length=4, max_length=60, required=False)
    last_name = serializers.CharField(min_length=4, max_length=60, required=False)
    phone = serializers.CharField(max_length=15, required=False, allow_blank=True)
    mobile = serializers.CharField(max_length=15, required=False, allow_blank=True)
    address = serializers.CharField(max_length=200, required=False, allow_blank=True)
    city = serializers.CharField(max_length=200, required=False, allow_blank=True)
    state = serializers.CharField(max_length=200, required=False, allow_blank=True)
    zip_code = serializers.CharField(max_length=12, required=False, allow_blank=True)
    country = serializers.CharField(max_length=200, required=False, allow_blank=True)
    birth = serializers.DateField(required=False, allow_null=True)
    title = serializers.CharField(max_length=100, required=False, allow_blank=True)
    about = serializers.CharField(max_length=250, required=False, allow_blank=True)

    # Change password fields
    id = serializers.IntegerField(required=False)
    current_password = serializers.CharField(write_only=True, required=False)

    # Forgot password fields
    forgot_email = serializers.EmailField(required=False)
    
    # JWT refresh token field
    access = serializers.CharField(required=False, write_only=True)
    refresh = serializers.CharField(required=False, write_only=True)
    token = serializers.CharField(required=False, write_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        action = self.context.get('action')

        if action == 'register':
            for field in ['username', 'password', 'repeat_password', 'email', 'first_name', 'last_name']:
                self.fields[field].required = True
        elif action == 'login':
            for field in ['username', 'password']:
                self.fields[field].required = True
        elif action == 'change_password':
            for field in ['id', 'current_password', 'password', 'repeat_password']:
                self.fields[field].required = True
        elif action == 'admin_change_password':
            for field in ['id', 'password', 'repeat_password']:
                self.fields[field].required = True
        elif action == 'forgot_password':
            self.fields['forgot_email'].required = True
        elif action == 'access_token':
            for field in ['username', 'password']:
                self.fields[field].required = True
        elif action == 'refresh_token':
            self.fields['refresh'].required = True
        elif action == 'verify_token':
            self.fields['token'].required = True

    def validate(self, data):
        return AuthService.validate(self, User, data)

    def register(self):
        return AuthService.register(
            self,
            UserSerializer,
            UserProfileSerializer
        )

    def login(self):
        return AuthService.login(
            self,
            UserSerializer
        )

    def change_password(self):
        return AuthService.change_password(self)

    def admin_change_password(self):
        return AuthService.admin_change_password(self)

    def forgot_password(self):
        return AuthService.forgot_password(self)

    def access_token(self):
        return AuthService.access_token(
            self,
            AuthTokenObtainPairSerializer
        )

    def refresh_token(self):
        return AuthService.refresh_token(
            self,
            AuthTokenRefreshSerializer
        )

    def verify_token(self):
        return AuthService.verify_token(
            self,
            AuthTokenVerifySerializer
        )


class AuthTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        # Custom data to include in the response
        data['user'] = UserSerializer(user).data
        data['exp'] = data.get('access', None) and AccessToken(data['access']).payload.get('exp', None)
        return data


class AuthTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        from rest_framework_simplejwt.exceptions import TokenError
        try:
            data = super().validate(attrs)
            access_token = data.get('access', None)

            user = None
            token_obj = None
            if access_token:
                try:
                    token_obj = AccessToken(access_token)
                    user_id = token_obj.get('user_id')
                    user = User.objects.filter(id=user_id).first()
                except TokenError as e:
                    raise serializers.ValidationError({'detail': str(e)})
            else:
                raise serializers.ValidationError({'detail': 'Access token is required.'})

            if user:
                data['user'] = UserSerializer(user).data
                data['exp'] = token_obj.payload.get('exp', None)

            return data
        except TokenError as e:
            raise serializers.ValidationError({'detail': str(e)})


class AuthTokenVerifySerializer(TokenVerifySerializer):
    def validate(self, attrs):
        return super().validate(attrs)


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for django default user data.
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name',
                  'last_name', 'is_active', 'is_staff',
                  'is_superuser', 'date_joined', 'last_login')

    def to_representation(self, instance):
        """
        Customize the representation of the user data.
        """
        data = super().to_representation(instance)
        if hasattr(instance, "id"):
            data["id"] = instance.id
        data["username"] = getattr(instance, "username", data.get("username", None))
        data["email"] = getattr(instance, "email", data.get("email", None))
        data["first_name"] = getattr(instance, "first_name", data.get("first_name", None))
        data["last_name"] = getattr(instance, "last_name", data.get("last_name", None))
        data["is_staff"] = getattr(instance, "is_staff", False)
        data["is_superuser"] = getattr(instance, "is_superuser", False)
        user_profile = UserProfile.objects.filter(user=instance).first() if hasattr(instance, "id") else None
        if user_profile:
            data["avatar"] = user_profile.avatar.url if user_profile.avatar else None
        return data


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for extended user profile data.
    """
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = (
            'avatar', 'phone', 'mobile', 'address', 'city', 'state', 'zip_code', 'country', 'birth', 'title', 'about'
        )

    def get_avatar(self, obj):
        """
        Get the avatar URL for the user profile.
        """
        if obj.avatar:
            return obj.avatar.url
        return None


class UserExtendedSerializer(serializers.ModelSerializer):
    """
    Serializer for extended user profile data.
    """
    avatar = serializers.SerializerMethodField()
    phone = serializers.CharField(source='profile.phone', required=False, allow_blank=True)
    mobile = serializers.CharField(source='profile.mobile', required=False, allow_blank=True)
    address = serializers.CharField(source='profile.address', required=False, allow_blank=True)
    city = serializers.CharField(source='profile.city', required=False, allow_blank=True)
    state = serializers.CharField(source='profile.state', required=False, allow_blank=True)
    zip_code = serializers.CharField(source='profile.zip_code', required=False, allow_blank=True)
    country = serializers.CharField(source='profile.country', required=False, allow_blank=True)
    birth = serializers.DateField(source='profile.birth', required=False, allow_null=True)
    title = serializers.CharField(source='profile.title', required=False, allow_blank=True)
    about = serializers.CharField(source='profile.about', required=False, allow_blank=True)

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name', 'is_active',
            'is_staff', 'is_superuser', 'date_joined', 'last_login',
            'avatar', 'title', 'phone', 'mobile', 'address', 'city', 'state',
            'zip_code', 'country', 'birth', 'about'
        )

    def validate_username(self, value):
        """
        Validate the username field.
        """
        user = self.instance
        if User.objects.exclude(pk=user.pk if user else None).filter(username=value).exists():
            raise serializers.ValidationError("A user with that username already exists.")
        return value

    def validate_email(self, value):
        """
        Validate the email field.
        """
        user = self.instance
        if User.objects.exclude(pk=user.pk if user else None).filter(email=value).exists():
            raise serializers.ValidationError("A user with that email already exists.")
        return value

    def get_avatar(self, obj):
        """
        Get the avatar URL for the user.
        """
        profile = getattr(obj, 'profile', None)
        if profile and profile.avatar:
            if profile and hasattr(profile.avatar, 'url'):
                return profile.avatar.url
            else:
                return profile.avatar
        return None
    
    def update(self, instance, validated_data):
        """
        Update user and user profile data.
        """
        profile_data = validated_data.pop('profile', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if profile_data:
            profile = getattr(instance, 'profile', None)
            if profile:
                for attr, value in profile_data.items():
                    setattr(profile, attr, value)
                profile.save()
        return instance
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        profile = getattr(instance, 'profile', None)

        # Set empty string or None for missing fields
        fields = [
            'avatar', 'title', 'phone', 'mobile', 'address', 'city', 'state',
            'zip_code', 'country', 'birth', 'about'
        ]

        # Avatar
        if profile and profile.avatar:
            data['avatar'] = profile.avatar.url if hasattr(profile.avatar, 'url') else profile.avatar
        else:
            data['avatar'] = ''

        # Other profile fields
        for field in fields:
            if field == 'avatar':
                continue
            value = getattr(profile, field, '') if profile else ''
            if value is None:
                value = ''
            data[field] = value

        return data


class LocationZonesSerializer(serializers.ModelSerializer):
    """
    Serializer for location zones.
    """
    creator = UserSerializer(read_only=True)
    updater = UserSerializer(read_only=True)
    locations = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = LocationZones
        fields = ('id', 'title', 'description', 'code_name', 'status',
            'is_core', 'manager', 'manager_email', 'manager_phone',
            'manager_mobile', 'sort_order', 'creator', 'updater',
            'created_at', 'updated_at', 'locations')
        read_only_fields = ('is_core', 'creator', 'created_at',
                            'updater', 'updated_at')
        
    title = serializers.CharField(required=False)

    def __init__(self, *args, **kwargs):
        """
        Initialize the serializer and adjust required fields based on action in context.
        """
        super().__init__(*args, **kwargs)
        action = self.context.get('action')

        if action == 'locations':
            self.fields['title'].required = False
        else:
            self.fields['title'].required = True

    def validate(self, data):
        """
        Validates the data before creating or updating a location zone.
        If an attempt is made to edit a record with is_core=True and the user is not a superadmin, raises an error.
        If is_core is not provided, it forces it to False.
        """
        action = self.context.get('action')
        request = self.context.get('request')
        instance = getattr(self, 'instance', None)
        
        if action != 'locations':
            # If this is an update, check if it is core and if the user is NOT admin
            if instance and getattr(instance, 'is_core', False):
                if not request or not getattr(request.user, 'is_superuser', False):
                    raise serializers.ValidationError({'detail': 'Only superadmins can edit core device builds.'})

        return data

    @classmethod
    def get_queryset(cls, request):
        """
        Returns the queryset for location zones, applying filters using LocationZonesFilter.
        """
        queryset = LocationZones.objects.all()
        filterset = LocationZonesFilter(request.GET, queryset=queryset)
        return filterset.qs

    @classmethod
    def get_locations_by_location_zone(cls, request, id=None):
        """
        Returns the list of locations by location zone ID.
        """
        '''
        if id:
            items = Locations.objects.filter(location_zone=id)
            serializer = LocationsSerializer(items, many=True)
            return serializer.data
        '''
        if id:
            items = Locations.objects.filter(location_zone=id)
            paginator = DefaultLimitOffsetPagination()
            paginated_items = paginator.paginate_queryset(items, request)
            serializer = LocationsSerializer(paginated_items, many=True)
            paginated_response = paginator.get_paginated_response(serializer.data)
            return paginated_response.data
        return []

    @classmethod
    def create_location_zone(cls, request):
        """
        Creates a location zone.
        """
        serializer = cls(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(
                creator=request.user,
                created_at=timezone.now(),
                updater=None,
                updated_at=None,
                status=1,
            )
            return serializer.data, None
        return None, serializer.errors

    @classmethod
    def update_location_zone(cls, request, pk, partial=False):
        """
        Updates a location zone.
        """
        instance = LocationZones.objects.filter(pk=pk).first()
        if not instance:
            return None, {'detail': 'Not found.'}
        serializer = cls(instance, data=request.data, context={'request': request}, partial=partial)
        if serializer.is_valid():
            serializer.save(
                updater=request.user,
                updated_at=timezone.now(),
            )
            return serializer.data, None
        return None, serializer.errors
    
    def to_representation(self, instance):
        """
        Customize the representation of the location zone data.
        """
        data = super().to_representation(instance)
        data["locations_count"] = Locations.objects.filter(location_zone=instance).count()
        return data


class LocationsSerializer(serializers.ModelSerializer):
    """
    Serializer for locations.
    """
    location_zone = serializers.SerializerMethodField()
    creator = UserSerializer(read_only=True)
    updater = UserSerializer(read_only=True)
    
    location_zone_id = serializers.PrimaryKeyRelatedField(
        queryset=LocationZones.objects.all(),
        source='location_zone',
        write_only=True
    )

    class Meta:
        model = Locations
        fields = ('id', 'title', 'description', 'code_name', 'status',
                  'is_core', 'location_zone', 'location_zone_id',
                  'manager', 'manager_email', 'manager_phone',
                  'manager_mobile', 'collaborator', 'collaborator_email',
                  'collaborator_phone', 'collaborator_mobile', 'phone',
                  'mobile', 'address', 'city', 'state', 'zip_code',
                  'country', 'latitude', 'longitude', 'sort_order',
                  'creator', 'updater', 'created_at', 'updated_at')
        read_only_fields = ('is_core', 'creator', 'created_at',
                            'updater', 'updated_at')

    def get_location_zone(self, obj):
        return {
            'id': obj.location_zone.id,
            'title': obj.location_zone.title,
            'description': obj.location_zone.description
        }

    def validate(self, data):
        """
        Validates the data before creating or updating a location.
        If an attempt is made to edit a record with is_core=True and the user is not a superadmin, raises an error.
        If is_core is not provided, it forces it to False.
        """
        request = self.context.get('request')
        instance = getattr(self, 'instance', None)

        # If this is an update, check if it is core and if the user is NOT admin
        if instance and getattr(instance, 'is_core', False):
            if not request or not getattr(request.user, 'is_superuser', False):
                raise serializers.ValidationError({'detail': 'Only superadmins can edit core device builds.'})

        return data

    @classmethod
    def get_queryset(cls, request):
        """
        Returns the queryset for locations, applying filters using LocationsFilter.
        """
        queryset = Locations.objects.all()
        filterset = LocationsFilter(request.GET, queryset=queryset)
        return filterset.qs

    @classmethod
    def create_location(cls, request):
        """
        Creates a location.
        """
        serializer = cls(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(
                creator=request.user,
                created_at=timezone.now(),
                updater=None,
                updated_at=None,
                status=1,
            )
            return serializer.data, None
        return None, serializer.errors

    @classmethod
    def update_location(cls, request, pk, partial=False):
        """
        Updates a location.
        """
        instance = Locations.objects.filter(pk=pk).first()
        if not instance:
            return None, {'detail': 'Not found.'}
        serializer = cls(instance, data=request.data, context={'request': request}, partial=partial)
        if serializer.is_valid():
            serializer.save(
                updater=request.user,
                updated_at=timezone.now(),
            )
            return serializer.data, None
        return None, serializer.errors

    def to_representation(self, instance):
        """
        Customize the representation of the location data.
        """
        data = super().to_representation(instance)
        data["devices_count"] = Devices.objects.filter(location=instance).count()
        return data


class DeviceTypesSerializer(serializers.ModelSerializer):
    """
    Serializer for device types.
    """
    creator = UserSerializer(read_only=True)
    updater = UserSerializer(read_only=True)

    class Meta:
        model = DeviceTypes
        fields = ('id', 'title', 'description', 'code_name', 'status',
                  'is_core', 'is_deprecated', 'sort_order', 'creator',
                  'updater', 'created_at', 'updated_at')
        read_only_fields = ('is_core', 'creator', 'created_at',
                            'updater', 'updated_at')

    def validate(self, data):
        """
        Validates the data before creating or updating a device type.
        If an attempt is made to edit a record with is_core=True and the user is not a superadmin, raises an error.
        If is_core is not provided, it forces it to False.
        """
        request = self.context.get('request')
        instance = getattr(self, 'instance', None)

        # If this is an update, check if it is core and if the user is NOT admin
        if instance and getattr(instance, 'is_core', False):
            if not request or not getattr(request.user, 'is_superuser', False):
                raise serializers.ValidationError({'detail': 'Only superadmins can edit core device builds.'})

        return data

    @classmethod
    def get_queryset(cls, request):
        """
        Returns the queryset for device types, applying filters using DeviceTypesFilter.
        """
        queryset = DeviceTypes.objects.all()
        filterset = DeviceTypesFilter(request.GET, queryset=queryset)
        return filterset.qs

    @classmethod
    def create_type(cls, request):
        """
        Creates a device type.
        """
        serializer = cls(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(
                creator=request.user,
                created_at=timezone.now(),
                updater=None,
                updated_at=None,
                status=1,
            )
            return serializer.data, None
        return None, serializer.errors

    @classmethod
    def update_type(cls, request, pk, partial=False):
        """
        Updates a device type.
        """
        instance = DeviceTypes.objects.filter(pk=pk).first()
        if not instance:
            return None, {'detail': 'Not found.'}
        serializer = cls(instance, data=request.data, context={'request': request}, partial=partial)
        if serializer.is_valid():
            serializer.save(
                updater=request.user,
                updated_at=timezone.now(),
            )
            return serializer.data, None
        return None, serializer.errors


class DeviceMarksSerializer(serializers.ModelSerializer):
    """
    Serializer for device marks.
    """
    creator = UserSerializer(read_only=True)
    updater = UserSerializer(read_only=True)

    class Meta:
        model = DeviceMarks
        fields = ('id', 'title', 'description', 'code_name', 'status',
                  'is_core', 'is_deprecated', 'sort_order', 'creator',
                  'updater', 'created_at', 'updated_at')
        read_only_fields = ('is_core', 'creator', 'created_at',
                            'updater', 'updated_at')

    def validate(self, data):
        """
        Validates the data before creating or updating a device mark.
        If an attempt is made to edit a record with is_core=True and the user is not a superadmin, raises an error.
        If is_core is not provided, it forces it to False.
        """
        request = self.context.get('request')
        instance = getattr(self, 'instance', None)

        # If this is an update, check if it is core and if the user is NOT admin
        if instance and getattr(instance, 'is_core', False):
            if not request or not getattr(request.user, 'is_superuser', False):
                raise serializers.ValidationError({'detail': 'Only superadmins can edit core device builds.'})

        return data

    @classmethod
    def get_queryset(cls, request):
        """
        Returns the queryset for device marks, applying filters using DeviceMarksFilter.
        """
        queryset = DeviceMarks.objects.all()
        filterset = DeviceMarksFilter(request.GET, queryset=queryset)
        return filterset.qs

    @classmethod
    def create_mark(cls, request):
        """
        Creates a device mark.
        """
        serializer = cls(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(
                creator=request.user,
                created_at=timezone.now(),
                updater=None,
                updated_at=None,
                status=1,
            )
            return serializer.data, None
        return None, serializer.errors

    @classmethod
    def update_mark(cls, request, pk, partial=False):
        """
        Updates a device mark.
        """
        instance = DeviceMarks.objects.filter(pk=pk).first()
        if not instance:
            return None, {'detail': 'Not found.'}
        serializer = cls(instance, data=request.data, context={'request': request}, partial=partial)
        if serializer.is_valid():
            serializer.save(
                updater=request.user,
                updated_at=timezone.now(),
            )
            return serializer.data, None
        return None, serializer.errors


class DeviceModelsSerializer(serializers.ModelSerializer):
    """
    Serializer for device models.
    """
    creator = UserSerializer(read_only=True)
    updater = UserSerializer(read_only=True)

    class Meta:
        model = DeviceModels
        fields = ('id', 'title', 'description', 'code_name', 'status',
                  'is_core', 'is_deprecated', 'sort_order', 'creator',
                  'updater', 'created_at', 'updated_at')
        read_only_fields = ('is_core', 'creator', 'created_at',
                            'updater', 'updated_at')

    def validate(self, data):
        """
        Validates the data before creating or updating a device model.
        If an attempt is made to edit a record with is_core=True and the user is not a superadmin, raises an error.
        If is_core is not provided, it forces it to False.
        """
        request = self.context.get('request')
        instance = getattr(self, 'instance', None)

        # If this is an update, check if it is core and if the user is NOT admin
        if instance and getattr(instance, 'is_core', False):
            if not request or not getattr(request.user, 'is_superuser', False):
                raise serializers.ValidationError({'detail': 'Only superadmins can edit core device builds.'})

        return data

    @classmethod
    def get_queryset(cls, request):
        """
        Returns the queryset for device models, applying filters using DeviceModelsFilter.
        """
        queryset = DeviceModels.objects.all()
        filterset = DeviceModelsFilter(request.GET, queryset=queryset)
        return filterset.qs

    @classmethod
    def create_model(cls, request):
        """
        Creates a device model.
        """
        serializer = cls(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(
                creator=request.user,
                created_at=timezone.now(),
                updater=None,
                updated_at=None,
                status=1,
            )
            return serializer.data, None
        return None, serializer.errors

    @classmethod
    def update_model(cls, request, pk, partial=False):
        """
        Updates a device model.
        """
        instance = DeviceModels.objects.filter(pk=pk).first()
        if not instance:
            return None, {'detail': 'Not found.'}
        serializer = cls(instance, data=request.data, context={'request': request}, partial=partial)
        if serializer.is_valid():
            serializer.save(
                updater=request.user,
                updated_at=timezone.now(),
            )
            return serializer.data, None
        return None, serializer.errors


class DeviceSystemsSerializer(serializers.ModelSerializer):
    """
    Serializer for device systems.
    """
    creator = UserSerializer(read_only=True)
    updater = UserSerializer(read_only=True)

    class Meta:
        model = DeviceSystems
        fields = ('id', 'title', 'description', 'code_name', 'status',
                  'is_core', 'is_deprecated', 'sort_order', 'creator',
                  'updater', 'created_at', 'updated_at')
        read_only_fields = ('is_core', 'creator', 'created_at',
                            'updater', 'updated_at')

    def validate(self, data):
        """
        Validates the data before creating or updating a device system.
        If an attempt is made to edit a record with is_core=True and the user is not a superadmin, raises an error.
        If is_core is not provided, it forces it to False.
        """
        request = self.context.get('request')
        instance = getattr(self, 'instance', None)

        # If this is an update, check if it is core and if the user is NOT admin
        if instance and getattr(instance, 'is_core', False):
            if not request or not getattr(request.user, 'is_superuser', False):
                raise serializers.ValidationError({'detail': 'Only superadmins can edit core device builds.'})

        return data

    @classmethod
    def get_queryset(cls, request):
        """
        Returns the queryset for device system, applying filters using DeviceSystemsFilter.
        """
        queryset = DeviceSystems.objects.all()
        filterset = DeviceSystemsFilter(request.GET, queryset=queryset)
        return filterset.qs

    @classmethod
    def create_system(cls, request):
        """
        Creates a device system.
        """
        serializer = cls(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(
                creator=request.user,
                created_at=timezone.now(),
                updater=None,
                updated_at=None,
                status=1,
            )
            return serializer.data, None
        return None, serializer.errors

    @classmethod
    def update_system(cls, request, pk, partial=False):
        """
        Updates a device system.
        """
        instance = DeviceSystems.objects.filter(pk=pk).first()
        if not instance:
            return None, {'detail': 'Not found.'}
        serializer = cls(instance, data=request.data, context={'request': request}, partial=partial)
        if serializer.is_valid():
            serializer.save(
                updater=request.user,
                updated_at=timezone.now(),
            )
            return serializer.data, None
        return None, serializer.errors


class DeviceBuildsSerializer(serializers.ModelSerializer):
    """
    Serializer for device builds.
    """
    creator = UserSerializer(read_only=True)
    updater = UserSerializer(read_only=True)

    class Meta:
        model = DeviceBuilds
        fields = ('id', 'title', 'description', 'code_name', 'status',
                  'is_core', 'is_deprecated', 'sort_order', 'creator',
                  'updater', 'created_at', 'updated_at')
        read_only_fields = ('is_core', 'creator', 'created_at',
                            'updater', 'updated_at')

    def validate(self, data):
        """
        Validates the data before creating or updating a device build.
        If an attempt is made to edit a record with is_core=True and the user is not a superadmin, raises an error.
        If is_core is not provided, it forces it to False.
        """
        # If this is an update, check if it is core and if the user is NOT admin
        if self.instance and self.instance.is_core:
            request = self.context.get('request')
            if not request or not hasattr(request, 'user'):
                raise serializers.ValidationError(
                    'Request context is missing for validation.'
                )

            if not request.user.is_superuser:
                raise serializers.ValidationError(
                    f'Only superadmins can edit core device builds. username: {request.user.username}. is_superuser: {request.user.is_superuser}'
                )

        return data

    @classmethod
    def get_queryset(cls, request):
        """
        Returns the queryset for device builds, applying filters using DeviceBuildsFilter.
        """
        queryset = DeviceBuilds.objects.all()
        filterset = DeviceBuildsFilter(request.GET, queryset=queryset)
        return filterset.qs

    @classmethod
    def create_build(cls, request):
        """
        Creates a device build.
        """
        serializer = cls(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(
                creator=request.user,
                created_at=timezone.now(),
                updater=None,
                updated_at=None,
                status=1,
            )
            return serializer.data, None
        return None, serializer.errors

    @classmethod
    def update_build(cls, request, pk, partial=False):
        """
        Updates a device build.
        """
        instance = DeviceBuilds.objects.filter(pk=pk).first()
        if not instance:
            return None, {'detail': 'Not found.'}
        serializer = cls(instance, data=request.data, context={'request': request}, partial=partial)
        if serializer.is_valid():
            serializer.save(
                updater=request.user,
                updated_at=timezone.now(),
            )
            return serializer.data, None
        return None, serializer.errors


class DeviceProcessorsSerializer(serializers.ModelSerializer):
    """
    Serializer for device processors.
    """
    creator = UserSerializer(read_only=True)
    updater = UserSerializer(read_only=True)

    class Meta:
        model = DeviceProcessors
        fields = ('id', 'title', 'description', 'code_name', 'status',
                  'is_core', 'is_deprecated', 'sort_order', 'creator',
                  'updater', 'created_at', 'updated_at')
        read_only_fields = ('is_core', 'creator', 'created_at',
                            'updater', 'updated_at')

    def validate(self, data):
        """
        Validates the data before creating or updating a device processor.
        If an attempt is made to edit a record with is_core=True and the user is not a superadmin, raises an error.
        If is_core is not provided, it forces it to False.
        """
        request = self.context.get('request')
        instance = getattr(self, 'instance', None)

        # If this is an update, check if it is core and if the user is NOT admin
        if instance and getattr(instance, 'is_core', False):
            if not request or not getattr(request.user, 'is_superuser', False):
                raise serializers.ValidationError({'detail': 'Only superadmins can edit core device builds.'})

        return data

    @classmethod
    def get_queryset(cls, request):
        """
        Returns the queryset for device processors, applying filters using DeviceProcessorsFilter.
        """
        queryset = DeviceProcessors.objects.all()
        filterset = DeviceProcessorsFilter(request.GET, queryset=queryset)
        return filterset.qs

    @classmethod
    def create_processor(cls, request):
        """
        Creates a device processor.
        """
        serializer = cls(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(
                creator=request.user,
                created_at=timezone.now(),
                updater=None,
                updated_at=None,
                status=1,
            )
            return serializer.data, None
        return None, serializer.errors

    @classmethod
    def update_processor(cls, request, pk, partial=False):
        """
        Updates a device processor.
        """
        instance = DeviceProcessors.objects.filter(pk=pk).first()
        if not instance:
            return None, {'detail': 'Not found.'}
        serializer = cls(instance, data=request.data, context={'request': request}, partial=partial)
        if serializer.is_valid():
            serializer.save(
                updater=request.user,
                updated_at=timezone.now(),
            )
            return serializer.data, None
        return None, serializer.errors


class DeviceRAMsSerializer(serializers.ModelSerializer):
    """
    Serializer for device RAMs.
    """
    creator = UserSerializer(read_only=True)
    updater = UserSerializer(read_only=True)

    class Meta:
        model = DeviceRAMs
        fields = ('id', 'title', 'description', 'code_name', 'status',
                  'is_core', 'is_deprecated', 'sort_order', 'creator',
                  'updater', 'created_at', 'updated_at')
        read_only_fields = ('is_core', 'creator', 'created_at',
                            'updater', 'updated_at')

    def validate(self, data):
        """
        Validates the data before creating or updating a device RAM.
        If an attempt is made to edit a record with is_core=True and the user is not a superadmin, raises an error.
        If is_core is not provided, it forces it to False.
        """
        request = self.context.get('request')
        instance = getattr(self, 'instance', None)

        # If this is an update, check if it is core and if the user is NOT admin
        if instance and getattr(instance, 'is_core', False):
            if not request or not getattr(request.user, 'is_superuser', False):
                raise serializers.ValidationError({'detail': 'Only superadmins can edit core device builds.'})

        return data

    @classmethod
    def get_queryset(cls, request):
        """
        Returns the queryset for device RAMs, applying filters using DeviceRAMsFilter.
        """
        queryset = DeviceRAMs.objects.all()
        filterset = DeviceRAMsFilter(request.GET, queryset=queryset)
        return filterset.qs

    @classmethod
    def create_ram(cls, request):
        """
        Creates a device RAM.
        """
        serializer = cls(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(
                creator=request.user,
                created_at=timezone.now(),
                updater=None,
                updated_at=None,
                status=1,
            )
            return serializer.data, None
        return None, serializer.errors

    @classmethod
    def update_ram(cls, request, pk, partial=False):
        """
        Updates a device RAM.
        """
        instance = DeviceRAMs.objects.filter(pk=pk).first()
        if not instance:
            return None, {'detail': 'Not found.'}
        serializer = cls(instance, data=request.data, context={'request': request}, partial=partial)
        if serializer.is_valid():
            serializer.save(
                updater=request.user,
                updated_at=timezone.now(),
            )
            return serializer.data, None
        return None, serializer.errors


class DeviceDisksSerializer(serializers.ModelSerializer):
    """
    Serializer for device disks.
    """
    creator = UserSerializer(read_only=True)
    updater = UserSerializer(read_only=True)

    class Meta:
        model = DeviceDisks
        fields = ('id', 'title', 'description', 'code_name', 'status',
                  'is_core', 'is_deprecated', 'sort_order', 'creator',
                  'updater', 'created_at', 'updated_at')
        read_only_fields = ('is_core', 'creator', 'created_at',
                            'updater', 'updated_at')

    def validate(self, data):
        """
        Validates the data before creating or updating a device disk.
        If an attempt is made to edit a record with is_core=True and the user is not a superadmin, raises an error.
        If is_core is not provided, it forces it to False.
        """
        request = self.context.get('request')
        instance = getattr(self, 'instance', None)

        # If this is an update, check if it is core and if the user is NOT admin
        if instance and getattr(instance, 'is_core', False):
            if not request or not getattr(request.user, 'is_superuser', False):
                raise serializers.ValidationError({'detail': 'Only superadmins can edit core device builds.'})

        return data

    @classmethod
    def get_queryset(cls, request):
        """
        Returns the queryset for device disks, applying filters using DeviceDisksFilter.
        """
        queryset = DeviceDisks.objects.all()
        filterset = DeviceDisksFilter(request.GET, queryset=queryset)
        return filterset.qs

    @classmethod
    def create_disk(cls, request):
        """
        Creates a device disk.
        """
        serializer = cls(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(
                creator=request.user,
                created_at=timezone.now(),
                updater=None,
                updated_at=None,
                status=1,
            )
            return serializer.data, None
        return None, serializer.errors

    @classmethod
    def update_disk(cls, request, pk, partial=False):
        """
        Updates a device disk.
        """
        instance = DeviceDisks.objects.filter(pk=pk).first()
        if not instance:
            return None, {'detail': 'Not found.'}
        serializer = cls(instance, data=request.data, context={'request': request}, partial=partial)
        if serializer.is_valid():
            serializer.save(
                updater=request.user,
                updated_at=timezone.now(),
            )
            return serializer.data, None
        return None, serializer.errors

class SoftwaresSerializer(serializers.ModelSerializer):
    """
    Serializer for softwares.
    """
    creator = UserSerializer(read_only=True)
    updater = UserSerializer(read_only=True)

    class Meta:
        model = Softwares
        fields = ('id', 'title', 'description', 'version', 'code_name',
                  'status', 'is_core', 'is_deprecated', 'sort_order',
                  'creator', 'updater', 'created_at', 'updated_at')
        read_only_fields = ('is_core', 'creator', 'created_at',
                            'updater', 'updated_at')

    def validate(self, data):
        """
        Validates the data before creating or updating a software.
        If an attempt is made to edit a record with is_core=True and the user is not a superadmin, raises an error.
        If is_core is not provided, it forces it to False.
        """
        request = self.context.get('request')
        instance = getattr(self, 'instance', None)

        # If this is an update, check if it is core and if the user is NOT admin
        if instance and getattr(instance, 'is_core', False):
            if not request or not getattr(request.user, 'is_superuser', False):
                raise serializers.ValidationError({'detail': 'Only superadmins can edit core device builds.'})

        return data

    @classmethod
    def get_queryset(cls, request):
        """
        Returns the queryset for softwares, applying filters using SoftwaresFilter.
        """
        queryset = Softwares.objects.all()
        filterset = SoftwaresFilter(request.GET, queryset=queryset)
        return filterset.qs

    @classmethod
    def create_software(cls, request):
        """
        Creates a software.
        """
        serializer = cls(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(
                creator=request.user,
                created_at=timezone.now(),
                updater=None,
                updated_at=None,
                status=1,
            )
            return serializer.data, None
        return None, serializer.errors

    @classmethod
    def update_software(cls, request, pk, partial=False):
        """
        Updates a software.
        """
        instance = Softwares.objects.filter(pk=pk).first()
        if not instance:
            return None, {'detail': 'Not found.'}
        serializer = cls(instance, data=request.data, context={'request': request}, partial=partial)
        if serializer.is_valid():
            serializer.save(
                updater=request.user,
                updated_at=timezone.now(),
            )
            return serializer.data, None
        return None, serializer.errors


class DevicesSerializer(serializers.ModelSerializer):
    """
    Serializer for devices.
    """
    type = serializers.SerializerMethodField()
    mark = serializers.SerializerMethodField()
    model = serializers.SerializerMethodField()
    system = serializers.SerializerMethodField()
    build = serializers.SerializerMethodField()
    processor = serializers.SerializerMethodField()
    ram = serializers.SerializerMethodField()
    disk = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    creator = UserSerializer(read_only=True)
    updater = UserSerializer(read_only=True)
    
    type_id = serializers.PrimaryKeyRelatedField(
        queryset=DeviceTypes.objects.all(), 
        source='type',
        write_only=True
    )
    
    mark_id = serializers.PrimaryKeyRelatedField(
        queryset=DeviceMarks.objects.all(), 
        source='mark',
        write_only=True
    )
    
    model_id = serializers.PrimaryKeyRelatedField(
        queryset=DeviceModels.objects.all(),
        source='model',
        write_only=True
    )
    
    system_id = serializers.PrimaryKeyRelatedField(
        queryset=DeviceSystems.objects.all(),
        source='system',
        write_only=True
    )
    
    build_id = serializers.PrimaryKeyRelatedField(
        queryset=DeviceBuilds.objects.all(),
        source='build',
        write_only=True
    )
    
    processor_id = serializers.PrimaryKeyRelatedField(
        queryset=DeviceProcessors.objects.all(),
        source='processor',
        write_only=True
    )
    
    ram_id = serializers.PrimaryKeyRelatedField(
        queryset=DeviceRAMs.objects.all(),
        source='ram',
        write_only=True
    )
    
    disk_id = serializers.PrimaryKeyRelatedField(
        queryset=DeviceDisks.objects.all(),
        source='disk',
        write_only=True
    )
    
    location_id = serializers.PrimaryKeyRelatedField(
        queryset=Locations.objects.all(), 
        source='location', # Associates with the 'location' model
        write_only=True
    )

    class Meta:
        model = Devices
        fields = ('id', 'internal_id', 'hostname', 'status', 'type',
                  'type_id', 'mark', 'mark_id', 'model', 'model_id',
                  'system', 'system_id', 'build', 'build_id',
                  'processor', 'processor_id', 'ram',  'ram_id',
                  'disk', 'disk_id','disk_internal_id',
                  'disk_serial', 'network_ipv4', 'network_ipv6',
                  'network_mac', 'remote_id', 'serial', 'location',
                  'location_id', 'user_owner', 'notes',
                  'sort_order', 'creator', 'updater', 'created_at',
                  'updated_at')
        read_only_fields = ('creator', 'created_at',
                            'updater', 'updated_at')

    def get_type(self, obj):
        return {
            'id': obj.type.id,
            'title': obj.type.title,
            'description': obj.type.description
        }

    def get_mark(self, obj):
        return {
            'id': obj.mark.id,
            'title': obj.mark.title,
            'description': obj.mark.description
        }

    def get_model(self, obj):
        return {
            'id': obj.model.id,
            'title': obj.model.title,
            'description': obj.model.description
        }

    def get_system(self, obj):
        return {
            'id': obj.system.id,
            'title': obj.system.title,
            'description': obj.system.description
        }

    def get_build(self, obj):
        return {
            'id': obj.build.id,
            'title': obj.build.title,
            'description': obj.build.description
        }

    def get_processor(self, obj):
        return {
            'id': obj.processor.id,
            'title': obj.processor.title,
            'description': obj.processor.description
        }

    def get_ram(self, obj):
        return {
            'id': obj.ram.id,
            'title': obj.ram.title,
            'description': obj.ram.description
        }

    def get_disk(self, obj):
        return {
            'id': obj.disk.id,
            'title': obj.disk.title,
            'description': obj.disk.description
        }

    def get_location(self, obj):
        return {
            'id': obj.location.id,
            'title': obj.location.title,
            'description': obj.location.description
        }

    def validate(self, data):
        """
        Validates the data before creating or updating a device.
        """
        return data

    @classmethod
    def get_queryset(cls, request):
        """
        Returns the queryset for devices, applying filters using DevicesFilter.
        """
        queryset = Devices.objects.all()
        filterset = DevicesFilter(request.GET, queryset=queryset)
        return filterset.qs

    @classmethod
    def create_device(cls, request):
        """
        Creates a device.
        """
        serializer = cls(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(
                creator=request.user,
                created_at=timezone.now(),
                updater=None,
                updated_at=None,
                status=1,
            )
            return serializer.data, None
        return None, serializer.errors

    @classmethod
    def update_device(cls, request, pk, partial=False):
        """
        Updates a device.
        """
        instance = Devices.objects.filter(pk=pk).first()
        if not instance:
            return None, {'detail': 'Not found.'}
        serializer = cls(instance, data=request.data, context={'request': request}, partial=partial)
        if serializer.is_valid():
            serializer.save(
                updater=request.user,
                updated_at=timezone.now(),
            )
            return serializer.data, None
        return None, serializer.errors


class DeviceSoftwaresSerializer(serializers.ModelSerializer):
    """
    Serializer for device softwares (many-to-many relationship).
    """
    class Meta:
        model = DeviceSoftwares
        fields = ('id', 'device', 'software', 'installed_at')
        write_only_fields = ('installed_at')
        validators = [
            UniqueTogetherValidator(
                queryset=DeviceSoftwares.objects.all(),
                fields=['device', 'software']
            )
        ]

    @classmethod
    def get_queryset(cls, request):
        """
        Returns the queryset for device softwares, applying filters if needed.
        """
        queryset = DeviceSoftwares.objects.all()
        filterset = DeviceSoftwaresFilter(request.GET, queryset=queryset)
        return filterset.qs

    @classmethod
    def create_device_software(cls, request):
        """
        Creates a device software relation.
        """
        device_id = request.data.get('device_id')
        software_id = request.data.get('software_id')
        if not device_id or not software_id:
            raise ValueError("device_id and software_id are required")
        try:
            device = Devices.objects.get(id=device_id)
            software = Softwares.objects.get(id=software_id)
        except Devices.DoesNotExist:
            raise ValueError("Device does not exist")
        except Softwares.DoesNotExist:
            raise ValueError("Software does not exist")
        instance = DeviceSoftwares.objects.create(device=device, software=software)
        return instance

    @classmethod
    def update_device_software(cls, request, pk, partial=False):
        """
        Updates a device software relation.
        """
        instance = DeviceSoftwares.objects.get(pk=pk)
        software_id = request.data.get('software_id')
        if software_id:
            software = Softwares.objects.get(pk=software_id)
            instance.software = software
            instance.save()
        return instance

    
class NotificationTypesSerializer(serializers.ModelSerializer):
    """
    Serializer for notification types.
    """
    creator = UserSerializer(read_only=True)
    updater = UserSerializer(read_only=True)

    class Meta:
        model = NotificationTypes
        fields = ('id', 'title', 'description', 'status', 'is_core',
                  'creator', 'updater', 'created_at', 'updated_at')
        read_only_fields = ('is_core', 'creator', 'created_at',
                            'updater', 'updated_at')

    def validate(self, data):
        """
        Validates the data before creating or updating a notification type.
        If an attempt is made to edit a record with is_core=True and the user is not a superadmin, raises an error.
        If is_core is not provided, it forces it to False.
        """
        request = self.context.get('request')
        instance = getattr(self, 'instance', None)

        # If this is an update, check if it is core and if the user is NOT admin
        if instance and getattr(instance, 'is_core', False):
            if not request or not getattr(request.user, 'is_superuser', False):
                raise serializers.ValidationError({'detail': 'Only superadmins can edit core device builds.'})

        return data

    @classmethod
    def get_queryset(cls, request):
        """
        Returns the queryset for notification types, applying filters using NotificationTypesFilter.
        """
        queryset = NotificationTypes.objects.all()
        filterset = NotificationTypesFilter(request.GET, queryset=queryset)
        return filterset.qs

    @classmethod
    def create_notification_type(cls, request):
        """
        Creates a notification type.
        """
        serializer = cls(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(
                creator=request.user,
                created_at=timezone.now(),
                updater=None,
                updated_at=None,
                status=1,
            )
            return serializer.data, None
        return None, serializer.errors

    @classmethod
    def update_notification_type(cls, request, pk, partial=False):
        """
        Updates a notification type.
        """
        instance = NotificationTypes.objects.filter(pk=pk).first()
        if not instance:
            return None, {'detail': 'Not found.'}
        serializer = cls(instance, data=request.data, context={'request': request}, partial=partial)
        if serializer.is_valid():
            serializer.save(
                updater=request.user,
                updated_at=timezone.now(),
            )
            return serializer.data, None
        return None, serializer.errors

class NotificationsSerializer(serializers.ModelSerializer):
    """
    Serializer for notifications.
    """
    creator = UserSerializer(read_only=True)
    updater = UserSerializer(read_only=True)

    class Meta:
        model = Notifications
        fields = ('id', 'title', 'description', 'status', 
                  'type', 'module', 'module_id', 'creator',
                  'updater', 'created_at', 'updated_at')
        read_only_fields = ('creator', 'created_at',
                            'updater', 'updated_at')

    def validate(self, data):
        """
        Validates the data before creating or updating a notification.
        """
        return data

    @classmethod
    def get_queryset(cls, request):
        """
        Returns the queryset for notifications, applying filters using NotificationsFilter.
        """
        queryset = Notifications.objects.all()
        filterset = NotificationsFilter(request.GET, queryset=queryset)
        return filterset.qs

    @classmethod
    def create_notification(cls, request):
        """
        Creates a notification.
        """
        serializer = cls(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(
                creator=request.user,
                created_at=timezone.now(),
                updater=None,
                updated_at=None,
                status=1,
            )
            return serializer.data, None
        return None, serializer.errors

    @classmethod
    def update_notification(cls, request, pk, partial=False):
        """
        Updates a notification.
        """
        instance = Notifications.objects.filter(pk=pk).first()
        if not instance:
            return None, {'detail': 'Not found.'}
        serializer = cls(instance, data=request.data, context={'request': request}, partial=partial)
        if serializer.is_valid():
            serializer.save(
                updater=request.user,
                updated_at=timezone.now(),
            )
            return serializer.data, None
        return None, serializer.errors

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["type"] = instance.type.title

        return data


class AppSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppSettings
        fields = ('number_of_alerts', 'items_title_min_length',
                  'items_title_max_length', 'items_title_code_name_length',
                  'items_code_name_max_length', 'username_min_length',
                  'username_max_length', 'password_min_length',
                  'password_max_length', 'email_min_length',
                  'email_max_length', 'name_min_length', 'name_max_length',
                  'default_page_size', 'default_page_size_options',
                  'search_min_input_length', 'search_max_input_length',
                  'default_ordering_column', 'show_deprecated_only_in')
        read_only_fields = ('id',)


class UserSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSettings
        fields = ('default_language', 'default_theme', 'date_format_day',
            'date_format_month', 'date_format_year', 'timezone', 'time_24h')
        read_only_fields = ('id',)

