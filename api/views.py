from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from rest_framework import status, serializers, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from api.pagination import DefaultLimitOffsetPagination
from api.serializers import (
    AuthCustomSerializer, UserExtendedSerializer, LocationZonesSerializer,
    LocationsSerializer, DeviceTypesSerializer, DeviceMarksSerializer,
    DeviceModelsSerializer, DeviceSystemsSerializer, DeviceBuildsSerializer,
    DeviceProcessorsSerializer, DeviceRAMsSerializer,
    DeviceDisksSerializer, SoftwaresSerializer, DeviceSoftwaresSerializer,
    DevicesSerializer, NotificationTypesSerializer, NotificationsSerializer,
    AppSettingsSerializer, UserSettingsSerializer
)
from api.models import (
    Locations, Devices, Notifications, AppSettings, UserSettings
)
from api.filters import (
    UserExtendedFilter, LocationZonesFilter,
    LocationsFilter, DeviceTypesFilter, DeviceMarksFilter,
    DeviceModelsFilter, DeviceSystemsFilter, DeviceBuildsFilter,
    DeviceProcessorsFilter, DeviceRAMsFilter, DeviceDisksFilter,
    DevicesFilter, NotificationTypesFilter, NotificationsFilter
)


class AuthCustomViewSet(viewsets.GenericViewSet):
    """
    Custom authentication viewset for user registration, login, password change, and password reset.
    """
    permission_classes = [AllowAny]
    serializer_class = AuthCustomSerializer
    
    @action(detail=False, methods=['post'], url_path='register', permission_classes=[AllowAny])
    def register(self, request):
        """
        POST /auth/register/ - Endpoint for user registration.
        Expects: { "username": "...", "email": "...", "password": "...", "repeat_password": "...", "first_name": "...", "last_name": "..." }
        """
        serializer = AuthCustomSerializer(data=request.data, context={'action': 'register'})
        if serializer.is_valid():
            data = serializer.register()
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='login', permission_classes=[AllowAny])
    def login(self, request):
        """
        POST /auth/login/ - Endpoint for user login.
        Expects: { "username": "...", "password": "..." }
        """
        serializer = AuthCustomSerializer(data=request.data, context={'action': 'login'})
        if serializer.is_valid():
            data = serializer.login()
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='change-password', permission_classes=[IsAuthenticated])
    def change_password(self, request):
        """
        POST /auth/change-password/ - Endpoint for user password change.
        Expects: { "id": "...", "current_password": "...", "password": "...", "repeat_password": "..." }
        """
        serializer = AuthCustomSerializer(data=request.data, context={'action': 'change_password', 'request': request})
        if serializer.is_valid():
            data = serializer.change_password()
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='admin/change-password', permission_classes=[IsAdminUser])
    def admin_change_password(self, request):
        """
        POST /auth/admin/change-password/ - Endpoint for admins can change users passwords.
        Expects: { "id": "...", "password": "...", "repeat_password": "..." }
        """
        serializer = AuthCustomSerializer(data=request.data, context={'action': 'admin_change_password', 'request': request})
        if serializer.is_valid():
            data = serializer.admin_change_password()
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='forgot-password', permission_classes=[AllowAny])
    def forgot_password(self, request):
        """
        POST /auth/forgot-password/ - Endpoint for user password reset.
        Expects: { "forgot_email": "..." }
        """
        serializer = AuthCustomSerializer(data=request.data, context={'action': 'forgot_password', 'request': request})
        if serializer.is_valid():
            data = serializer.forgot_password()
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='token', permission_classes=[AllowAny])
    def access_token(self, request):
        """
        POST /auth/token/ - Endpoint for user token generation.
        Expects: { "username": "...", "password": "..." }
        """
        serializer = AuthCustomSerializer(data=request.data, context={'action': 'access_token'})
        if serializer.is_valid():
            data = serializer.access_token()
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='token/refresh', permission_classes=[AllowAny])
    def refresh_token(self, request):
        """
        POST /auth/token/refresh - Endpoint for refreshing user tokens.
        Expects: { "refresh": "..." }
        """
        serializer = AuthCustomSerializer(data=request.data, context={'action': 'refresh_token'})
        if serializer.is_valid():
            data = serializer.refresh_token()
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='token/verify', permission_classes=[AllowAny])
    def verify_token(self, request):
        """
        POST /auth/token/verify - Endpoint for verifying user tokens.
        Expects: { "token": "..." }
        """
        serializer = AuthCustomSerializer(data=request.data, context={'action': 'verify_token'})
        if serializer.is_valid():
            if serializer.verify_token():
                return Response({}, status=status.HTTP_200_OK)
            else:
                return Response({
                    'detail': 'Token is invalid.',
                    'code': 'token_not_valid'
                }, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserExtendedViewSet(viewsets.ModelViewSet):
    """
    User extended viewset. A merge of User and UserProfile models.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all().select_related('profile').filter()
    serializer_class = UserExtendedSerializer
    pagination_class = DefaultLimitOffsetPagination
    filter_backends = [OrderingFilter, ]
    filterset_class = UserExtendedFilter
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'list']:
            permission_classes = [permissions.IsAdminUser]
        elif self.action in ['retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def create_build(self, request):
        """
        POST /users/ - Endpoint for create a user with profile.
        """
        serializer = UserExtendedSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, partial=False):
        """
        PUT /users/{pk}/ - Endpoint for updates unified User and UserProfile data
        """
        user = self.get_object()
        serializer = UserExtendedSerializer(instance=user, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, pk=None, partial=False):
        """
        PATCH /profile/ - Endpoint for partially updates unified User and UserProfile data
        """
        user = self.get_object()
        serializer = UserExtendedSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk=None):
        """
        PATCH /profile/ - Endpoint for partially updates unified User and UserProfile data
        """
        return self.update(request, pk=pk, partial=True)

    def put(self, request, pk=None):
        """
        PUT /profile/ - Endpoint for updates unified User and UserProfile data
        """
        return self.update(request, pk)

    def to_representation(self, instance):
        """
        Custom representation for the UserExtendedSerializer.
        """
        data = super().to_representation(instance)
        return data


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    User profile viewset.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserExtendedSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_object(self):
        """
        GET /users/ - Endpoint for Returns the authenticated user.
        """
        return self.request.user
    
    def get_queryset(self):
        """
        GET /users/ - Endpoint for returns the queryset for the authenticated user's profile.
        """
        user = self.request.user
        return User.objects.filter(id=user.id)

    def list(self, request, *args, **kwargs):
        """
        GET /profile/ - Endpoint for returns unified Users and User Profile models for the authenticated user.
        """
        user = self.get_object()
        serializer = UserExtendedSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """
        GET /profile/ - Endpoint for returns unified User and User Profile models for the authenticated user.
        """
        user = self.get_object()
        serializer = UserExtendedSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None, partial=False):
        """
        POST /profile/ - Endpoint for updates unified User and User Profile models for the authenticated user.
        """
        user = self.get_object()
        serializer = UserExtendedSerializer(user, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None, partial=False):
        """
        PATCH /profile/ - Endpoint for partially updates unified User and User Profile models for the authenticated user.
        """
        user = self.get_object()
        serializer = UserExtendedSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk=None):
        """
        PATCH /profile/ - Endpoint for partially updates unified User and User Profile models for the authenticated user.
        """
        return self.update(request, pk=pk, partial=True)

    def put(self, request, pk=None):
        """
        PUT /profile/ - Endpoint for updates unified User and User Profile models for the authenticated user.
        """
        return self.update(request, pk)

    def destroy(self, request, pk=None):
        """
        DELETE /profile/ - Endpoint for deletes the authenticated user and their profile
        """
        raise serializers.ValidationError("You cannot delete your profile.")
    
    def delete(self, request, pk=None):
        """
        DELETE /profile/ - Endpoint for deletes the authenticated user and their profile
        """
        return self.destroy(request, pk)

    @action(detail=False, methods=['post'], url_path='upload-avatar', permission_classes=[IsAuthenticated], parser_classes=[MultiPartParser, FormParser])
    def upload_avatar(self, request):
        """
        POST /profile/upload-avatar/ - Endpoint to upload or change the authenticated user's avatar.
        """
        user = self.get_object()
        profile = getattr(user, 'profile', None)
        if not profile:
            return Response({'error': 'User profile not found.'}, status=status.HTTP_404_NOT_FOUND)
        file = request.FILES.get('avatar')
        if not file:
            return Response({'error': 'No file provided.'}, status=status.HTTP_400_BAD_REQUEST)
        profile.avatar = file
        profile.save()
        serializer = UserExtendedSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LocationZonesViewSet(ModelViewSet):
    """
    Location zones viewset.
    """
    serializer_class = LocationZonesSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = DefaultLimitOffsetPagination
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_class = LocationZonesFilter
    filterset_fields = ['location']

    def get_queryset(self):
        """
        GET /location-zones/ - Endpoint for get the list of location zones.
        """
        return LocationZonesSerializer.get_queryset(self.request)

    @action(detail=True, methods=['get'], url_path='locations', permission_classes=[AllowAny])
    def locations(self, request, pk=None):
        """
        GET /location-zones/{id}/locations/ - Endpoint for get the list of locations by location zone.
        Expects: { "id": "..." }
        """
        serializer = LocationZonesSerializer(data=request.data, context={'action': 'locations'})
        if serializer.is_valid():
            data = serializer.get_locations_by_location_zone(request, pk)
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        """
        POST /location-zones/ - Endpoint for create a location zone.
        """
        data, errors = LocationZonesSerializer.create_location_zone(request)
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, partial=False):
        """
        POST /location-zones/{pk}/ - Endpoint for update a location zone.
        """
        data, errors = LocationZonesSerializer.update_location_zone(request, pk, partial=partial)
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data, status=status.HTTP_200_OK)

    def patch(self, request, pk=None):
        """
        PATCH /location-zones/{pk}/ - Endpoint for partially update a location zone.
        """
        return self.update(request, pk=pk, partial=True)

    def put(self, request, pk=None):
        """
        PUT /location-zones/{pk}/ - Endpoint for updates a location zone.
        """
        return self.update(request, pk)


class LocationsViewSet(ModelViewSet):
    """
    Locations viewset.
    """
    serializer_class = LocationsSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = DefaultLimitOffsetPagination
    filter_backends = [OrderingFilter, ]
    filterset_class = LocationsFilter

    def get_queryset(self):
        """
        GET /locations/ - Endpoint for get the list of locations.
        """
        return LocationsSerializer.get_queryset(self.request)

    def get(self, request, id=None):
        """
        GET /locations/ or GET /locations/{id}/ - Endpoint for get the list of locations or a specific location by its ID.
        """
        if id:
            item = Locations.objects.get(id=id)
            serializer = LocationsSerializer(item)
            if serializer.is_valid():
                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        items = Locations.objects.all()
        serializer = LocationsSerializer(items, many=True)

        if serializer.is_valid():
            return Response({"status": "success", "data": self.paginate_queryset(serializer.data)}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        """
        POST /locations/ - Endpoint for create a location.
        """
        data, errors = LocationsSerializer.create_location(request)
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, partial=False):
        """
        POST /locations/{pk}/ - Endpoint for update a location.
        """
        data, errors = LocationsSerializer.update_location(request, pk, partial=partial)
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data, status=status.HTTP_200_OK)

    def patch(self, request, pk=None):
        """
        PATCH /locations/{pk}/ - Endpoint for partially update a location.
        """
        return self.update(request, pk=pk, partial=True)

    def put(self, request, pk=None):
        """
        PUT /locations/{pk}/ - Endpoint for updates a location.
        """
        return self.update(request, pk)


class DeviceTypesViewSet(ModelViewSet):
    """
    Device types viewset.
    """
    serializer_class = DeviceTypesSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = DefaultLimitOffsetPagination
    filter_backends = [OrderingFilter, ]
    filterset_class = DeviceTypesFilter

    def get_queryset(self):
        """
        GET /device-types/ - Endpoint for get the list of device types.
        """
        return DeviceTypesSerializer.get_queryset(self.request)

    def create(self, request):
        """
        POST /device-types/ - Endpoint for create a device type.
        """
        data, errors = DeviceTypesSerializer.create_type(request)
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, partial=False):
        """
        POST /device-types/{pk}/ - Endpoint for update a device type.
        """
        data, errors = DeviceTypesSerializer.update_type(request, pk, partial=partial)
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data, status=status.HTTP_200_OK)

    def patch(self, request, pk=None):
        """
        PATCH /device-types/{pk}/ - Endpoint for partially update a device type.
        """
        return self.update(request, pk=pk, partial=True)

    def put(self, request, pk=None):
        """
        PUT /device-types/{pk}/ - Endpoint for updates a device type.
        """
        return self.update(request, pk)


class DeviceMarksViewSet(ModelViewSet):
    """
    Device marks viewset.
    """
    serializer_class = DeviceMarksSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = DefaultLimitOffsetPagination
    filter_backends = [OrderingFilter, ]
    filterset_class = DeviceMarksFilter

    def get_queryset(self):
        """
        GET /device-marks/ - Endpoint for get the list of device marks.
        """
        return DeviceMarksSerializer.get_queryset(self.request)

    def create(self, request):
        """
        POST /device-marks/ - Endpoint for create a device mark.
        """
        data, errors = DeviceMarksSerializer.create_mark(request)
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, partial=False):
        """
        POST /device-marks/{pk}/ - Endpoint for update a device mark.
        """
        data, errors = DeviceMarksSerializer.update_mark(request, pk, partial=partial)
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data, status=status.HTTP_200_OK)

    def patch(self, request, pk=None):
        """
        PATCH /device-marks/{pk}/ - Endpoint for partially update a device mark.
        """
        return self.update(request, pk=pk, partial=True)

    def put(self, request, pk=None):
        """
        PUT /device-marks/{pk}/ - Endpoint for updates a device mark.
        """
        return self.update(request, pk)


class DeviceModelsViewSet(ModelViewSet):
    """
    Device models viewset.
    """
    serializer_class = DeviceModelsSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = DefaultLimitOffsetPagination
    filter_backends = [OrderingFilter, ]
    filterset_class = DeviceModelsFilter

    def get_queryset(self):
        """
        GET /device-models/ - Endpoint for get the list of device models.
        """
        return DeviceModelsSerializer.get_queryset(self.request)

    def create(self, request):
        """
        POST /device-models/ - Endpoint for create a device model.
        """
        data, errors = DeviceModelsSerializer.create_model(request)
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, partial=False):
        """
        POST /device-models/{pk}/ - Endpoint for update a device model.
        """
        data, errors = DeviceModelsSerializer.update_model(request, pk, partial=partial)
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data, status=status.HTTP_200_OK)

    def patch(self, request, pk=None):
        """
        PATCH /device-models/{pk}/ - Endpoint for partially update a device model.
        """
        return self.update(request, pk=pk, partial=True)

    def put(self, request, pk=None):
        """
        PUT /device-models/{pk}/ - Endpoint for updates a device model.
        """
        return self.update(request, pk)


class DeviceSystemsViewSet(ModelViewSet):
    """
    Device systems viewset.
    """
    serializer_class = DeviceSystemsSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = DefaultLimitOffsetPagination
    filter_backends = [OrderingFilter, ]
    filterset_class = DeviceSystemsFilter

    def get_queryset(self):
        """
        GET /device-systems/ - Endpoint for get the list of device systems.
        """
        return DeviceSystemsSerializer.get_queryset(self.request)

    def create(self, request):
        """
        POST /device-systems/ - Endpoint for create a device system.
        """
        data, errors = DeviceSystemsSerializer.create_system(request)
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, partial=False):
        """
        POST /device-systems/{pk}/ - Endpoint for update a device system.
        """
        data, errors = DeviceSystemsSerializer.update_system(request, pk, partial=partial)
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data, status=status.HTTP_200_OK)

    def patch(self, request, pk=None):
        """
        PATCH /device-systems/{pk}/ - Endpoint for partially update a device system.
        """
        return self.update(request, pk=pk, partial=True)

    def put(self, request, pk=None):
        """
        PUT /device-systems/{pk}/ - Endpoint for updates a device system.
        """
        return self.update(request, pk)


class DeviceBuildsViewSet(ModelViewSet):
    """
    Device builds viewset.
    """
    serializer_class = DeviceBuildsSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = DefaultLimitOffsetPagination
    filter_backends = [OrderingFilter, ]
    filterset_class = DeviceBuildsFilter
    
    def get_queryset(self):
        """
        GET /device-builds/ - Endpoint for get the list of device builds.
        """
        return DeviceBuildsSerializer.get_queryset(self.request)

    def create(self, request):
        """
        POST /device-builds/ - Endpoint for create a device build.
        """
        data, errors = DeviceBuildsSerializer.create_build(request)
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, partial=False):
        """
        POST /device-builds/{pk}/ - Endpoint for update a device build.
        """
        data, errors = DeviceBuildsSerializer.update_build(request, pk, partial=partial)
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data, status=status.HTTP_200_OK)

    def patch(self, request, pk=None):
        """
        PATCH /device-builds/{pk}/ - Endpoint for partially update a device build.
        """
        return self.update(request, pk=pk, partial=True)

    def put(self, request, pk=None):
        """
        PUT /device-builds/{pk}/ - Endpoint for updates a device build.
        """
        return self.update(request, pk)


class DeviceProcessorsViewSet(ModelViewSet):
    """
    Device processors viewset.
    """
    serializer_class = DeviceProcessorsSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = DefaultLimitOffsetPagination
    filter_backends = [OrderingFilter, ]
    filterset_class = DeviceProcessorsFilter

    def get_queryset(self):
        """
        GET /device-processors/ - Endpoint for get the list of device processors.
        """
        return DeviceProcessorsSerializer.get_queryset(self.request)

    def create(self, request):
        """
        POST /device-processors/ - Endpoint for create a device processor.
        """
        data, errors = DeviceProcessorsSerializer.create_processor(request)
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, partial=False):
        """
        POST /device-processors/{pk}/ - Endpoint for update a device processor.
        """
        data, errors = DeviceProcessorsSerializer.update_processor(request, pk, partial=partial)
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data, status=status.HTTP_200_OK)

    def patch(self, request, pk=None):
        """
        PATCH /device-processors/{pk}/ - Endpoint for partially update a device processor.
        """
        return self.update(request, pk=pk, partial=True)

    def put(self, request, pk=None):
        """
        PUT /device-processors/{pk}/ - Endpoint for updates a device processor.
        """
        return self.update(request, pk)


class DeviceRAMsViewSet(ModelViewSet):
    """
    Device RAMs viewset.
    """
    serializer_class = DeviceRAMsSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = DefaultLimitOffsetPagination
    filter_backends = [OrderingFilter, ]
    filterset_class = DeviceRAMsFilter

    def get_queryset(self):
        """
        GET /device-rams/ - Endpoint for get the list of device RAMs.
        """
        return DeviceRAMsSerializer.get_queryset(self.request)

    def create(self, request):
        """
        POST /device-rams/ - Endpoint for create a device RAM.
        """
        data, errors = DeviceRAMsSerializer.create_ram(request)
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, partial=False):
        """
        POST /device-rams/{pk}/ - Endpoint for update a device RAM.
        """
        data, errors = DeviceRAMsSerializer.update_ram(request, pk, partial=partial)
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data, status=status.HTTP_200_OK)

    def patch(self, request, pk=None):
        """
        PATCH /device-rams/{pk}/ - Endpoint for partially update a device RAM.
        """
        return self.update(request, pk=pk, partial=True)

    def put(self, request, pk=None):
        """
        PUT /device-rams/{pk}/ - Endpoint for updates a device RAM.
        """
        return self.update(request, pk)


class DeviceDisksViewSet(ModelViewSet):
    """
    Device disks viewset.
    """
    serializer_class = DeviceDisksSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = DefaultLimitOffsetPagination
    filter_backends = [OrderingFilter, ]
    filterset_class = DeviceDisksFilter

    def get_queryset(self):
        """
        GET /device-disks/ - Endpoint for get the list of device disks.
        """
        return DeviceDisksSerializer.get_queryset(self.request)

    def create(self, request):
        """
        POST /device-disks/ - Endpoint for create a device disk.
        """
        data, errors = DeviceDisksSerializer.create_disk(request)
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, partial=False):
        """
        POST /device-disks/{pk}/ - Endpoint for update a device disks.
        """
        data, errors = DeviceDisksSerializer.update_disk(request, pk, partial=partial)
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data, status=status.HTTP_200_OK)

    def patch(self, request, pk=None):
        """
        PATCH /device-disks/{pk}/ - Endpoint for partially update a device disk.
        """
        return self.update(request, pk=pk, partial=True)

    def put(self, request, pk=None):
        """
        PUT /device-disks/{pk}/ - Endpoint for updates a device disk.
        """
        return self.update(request, pk)


class SoftwaresViewSet(ModelViewSet):
    """
    Softwares viewset.
    """
    serializer_class = SoftwaresSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = DefaultLimitOffsetPagination
    filter_backends = [OrderingFilter, ]
    filterset_class = None

    def get_queryset(self):
        """
        GET /softwares/ - Endpoint for get the list of softwares.
        """
        return SoftwaresSerializer.get_queryset(self.request)

    def create(self, request):
        """
        POST /softwares/ - Endpoint for create a software.
        """
        data, errors = SoftwaresSerializer.create_software(request)
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, partial=False):
        """
        POST /softwares/{pk}/ - Endpoint for update a software.
        """
        data, errors = SoftwaresSerializer.update_software(request, pk, partial=partial)
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data, status=status.HTTP_200_OK)

    def patch(self, request, pk=None):
        """
        PATCH /softwares/{pk}/ - Endpoint for partially update a software.
        """
        return self.update(request, pk=pk, partial=True)

    def put(self, request, pk=None):
        """
        PUT /softwares/{pk}/ - Endpoint for updates a software.
        """
        return self.update(request, pk)


class DeviceSoftwaresViewSet(ModelViewSet):
    """
    DeviceSoftwares viewset.
    """
    serializer_class = DeviceSoftwaresSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = DefaultLimitOffsetPagination
    filter_backends = [OrderingFilter, ]

    def get_queryset(self):
        """
        GET /device-softwares/ - Endpoint for get the list of device softwares.
        """
        return DeviceSoftwaresSerializer.get_queryset(self.request)

    def create(self, request):
        """
        POST /device-softwares/ - Endpoint for create a device software relation.
        """
        data, errors = DeviceSoftwaresSerializer.create_device_software(request)
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, partial=False):
        """
        POST /device-softwares/{pk}/ - Endpoint for update a device software relation.
        """
        data, errors = DeviceSoftwaresSerializer.update_device_software(request, pk, partial=partial)
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data, status=status.HTTP_200_OK)

    def patch(self, request, pk=None):
        """
        PATCH /device-softwares/{pk}/ - Endpoint for partially update a device software relation.
        """
        return self.update(request, pk=pk, partial=True)

    def put(self, request, pk=None):
        """
        PUT /device-softwares/{pk}/ - Endpoint for updates a device software relation.
        """
        return self.update(request, pk)


class DevicesViewSet(ModelViewSet):
    """
    Devices viewset.
    """
    serializer_class = DevicesSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = DefaultLimitOffsetPagination
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_class = DevicesFilter
    filterset_fields = ['internal_id', 'location', 'type', 'mark', 'model',
                        'systems', 'builds', 'processor', 'ram', 'disk']

    def get_queryset(self):
        """
        GET /devices/ - Endpoint for get the list of devices.
        """
        return DevicesSerializer.get_queryset(self.request)

    def get(self, request, id=None):
        """
        GET /devices/ or GET /devices/{id}/ - Endpoint for get the list of devices or a specific device by its ID.
        """
        if id:
            item = Devices.objects.get(id=id)
            serializer = DevicesSerializer(item)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        items = Devices.objects.all()
        serializer = DevicesSerializer(items, many=True)
        return self.get_paginated_response({"status": "success", "data": self.paginate_queryset(serializer.data)})

    def create(self, request):
        """
        POST /devices/ - Endpoint for create a device.
        """
        data, errors = DevicesSerializer.create_device(request)
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, partial=False):
        """
        POST /devices/{pk}/ - Endpoint for update a device.
        """
        data, errors = DevicesSerializer.update_device(request, pk, partial=partial)
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data, status=status.HTTP_200_OK)

    def patch(self, request, pk=None):
        """
        PATCH /devices/{pk}/ - Endpoint for partially update a device.
        """
        return self.update(request, pk=pk, partial=True)

    def put(self, request, pk=None):
        """
        PUT /devices/{pk}/ - Endpoint for updates a device.
        """
        return self.update(request, pk)


class NotificationTypesViewSet(ModelViewSet):
    """
    Notification types viewset.
    """
    serializer_class = NotificationTypesSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = DefaultLimitOffsetPagination
    filter_backends = [OrderingFilter, ]
    filterset_class = NotificationTypesFilter

    def get_queryset(self):
        """
        GET /notification-types/ - Endpoint for get the list of notification types.
        """
        return NotificationTypesSerializer.get_queryset(self.request)

    def create(self, request):
        """
        POST /notification-types/ - Endpoint for create a notification type.
        Checks if is_core is True: only superadmins (user.is_superuser) can update.
        """
        data, errors = NotificationTypesSerializer.create_notification_type(request)
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, partial=False):
        """
        POST /notification-types/{pk}/ - Endpoint for update a notification type.
        Checks if is_core is True: only superadmins (user.is_superuser) can update.
        """
        data, errors = NotificationTypesSerializer.update_notification_type(request, pk, partial=partial)
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data, status=status.HTTP_200_OK)

    def patch(self, request, pk=None):
        """
        PATCH /notification-types/{pk}/ - Endpoint for partially update a notification type.
        """
        return self.update(request, pk=pk, partial=True)

    def put(self, request, pk=None):
        """
        PUT /notification-types/{pk}/ - Endpoint for updates a notification type.
        """
        return self.update(request, pk)


class NotificationsViewSet(ModelViewSet):
    """
    Notifications viewset.
    """
    serializer_class = NotificationsSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = DefaultLimitOffsetPagination
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_class = NotificationsFilter
    filterset_fields = ['status']

    def get_queryset(self):
        """
        GET /notifications/ - Endpoint for get the list of notifications.
        """
        return NotificationsSerializer.get_queryset(self.request)

    def get(self, request, id=None):
        """
        GET /notifications/ or GET /notifications/{id}/ - Endpoint for get the list of notifications or a specific notification by its ID.
        """
        if id:
            item = Notifications.objects.get(id=id)
            serializer = NotificationsSerializer(item)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        items = Notifications.objects.all()
        serializer = NotificationsSerializer(items, many=True)
        return self.get_paginated_response({"status": "success", "data": self.paginate_queryset(serializer.data)})

    def create(self, request):
        """
        POST /notifications/ - Endpoint for create a notification.
        """
        data, errors = NotificationsSerializer.create_notification(request)
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, partial=False):
        """
        POST /notifications/{pk}/ - Endpoint for update a notification.
        """
        data, errors = NotificationsSerializer.update_notification(request, pk, partial=partial)
        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data, status=status.HTTP_200_OK)

    def patch(self, request, pk=None):
        """
        PATCH /notifications/{pk}/ - Endpoint for partially update a notification.
        """
        return self.update(request, pk=pk, partial=True)


    def put(self, request, pk=None):
        """
        PUT /notifications/{pk}/ - Endpoint for updates a notification.
        """
        return self.update(request, pk)


class AppSettingsViewSet(ViewSet):
    """
    AppSettings viewset.
    """
    @method_decorator(cache_page(60 * 15))  # 15 minutes
    def list(self, request):
        settings = AppSettings.get_solo()
        serializer = AppSettingsSerializer(settings)
        return Response(serializer.data)


class UserSettingsViewSet(ViewSet):
    """
    UserSettings viewset.
    """
    @method_decorator(cache_page(60 * 15))  # 15 minutes
    @method_decorator(vary_on_cookie)
    def list(self, request):
        settings = UserSettings.get_solo()
        serializer = UserSettingsSerializer(settings)
        return Response(serializer.data)

