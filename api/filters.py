import django_filters

from api.models import (
    User, UserProfile, Locations, LocationZones, DeviceTypes, DeviceMarks,
    DeviceModels, DeviceSystems, DeviceProcessors, DeviceBuilds, DeviceRAMs,
    DeviceDisks, Softwares, Devices, DeviceSoftwares, NotificationTypes, Notifications
)


class UserExtendedFilter(django_filters.FilterSet):
    """
    Filter set for extended user data.
    """
    profile__phone = django_filters.CharFilter(field_name='profile__phone', lookup_expr='icontains')
    profile__mobile = django_filters.CharFilter(field_name='profile__mobile', lookup_expr='icontains')
    profile__address = django_filters.CharFilter(field_name='profile__address', lookup_expr='icontains')
    profile__city = django_filters.CharFilter(field_name='profile__city', lookup_expr='icontains')
    profile__state = django_filters.CharFilter(field_name='profile__state', lookup_expr='icontains')
    profile__zip_code = django_filters.CharFilter(field_name='profile__zip_code', lookup_expr='icontains')
    profile__country = django_filters.CharFilter(field_name='profile__country', lookup_expr='icontains')
    profile__birth = django_filters.DateFilter(field_name='profile__birth', lookup_expr='exact')
    profile__title = django_filters.CharFilter(field_name='profile__title', lookup_expr='icontains')
    profile__about = django_filters.CharFilter(field_name='profile__about', lookup_expr='icontains')

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'is_active',
            'is_staff', 'date_joined', 'last_login', 'profile__phone', 'profile__mobile',
            'profile__address', 'profile__city', 'profile__state', 'profile__zip_code',
            'profile__country', 'profile__birth', 'profile__title', 'profile__about'
        ]

class UsersFilter(django_filters.FilterSet):
    """
    Filter set for default django user data.
    """
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'is_active',
            'is_staff', 'date_joined', 'last_login'
        ]


class UsersProfileFilter(django_filters.FilterSet):
    """
    Filter set for user profile data.
    """
    class Meta:
        model = UserProfile
        fields = [
            'title', 'phone', 'mobile', 'address', 'city',
            'state', 'zip_code', 'country', 'birth', 'about'
        ]


class LocationZonesFilter(django_filters.FilterSet):
    """
    Filter set for location zone data.
    """
    class Meta:
        model = LocationZones
        fields = [
            'id', 'title', 'description', 'code_name', 'manager',
            'manager_email', 'manager_phone', 'manager_mobile',
            'creator', 'updater', 'created_at', 'updated_at'
        ]


class LocationsFilter(django_filters.FilterSet):
    """
    Filter set for location data.
    """
    ordering = django_filters.OrderingFilter(field_name='title')

    class Meta:
        model = Locations
        fields = [
            'id', 'title', 'description', 'code_name',
            'location_zone', 'manager', 'manager_email',
            'manager_phone', 'manager_mobile', 'collaborator',
            'collaborator_email', 'collaborator_phone',
            'collaborator_mobile', 'phone', 'mobile', 'address',
            'city', 'state', 'zip_code', 'country', 'latitude',
            'longitude', 'creator', 'updater', 'created_at',
            'updated_at'
            ]


class DeviceTypesFilter(django_filters.FilterSet):
    """
    Filter set for device types data.
    """
    class Meta:
        model = DeviceTypes
        fields = [
            'id', 'title', 'description', 'code_name',
            'is_deprecated', 'creator', 'updater',
            'created_at', 'updated_at'
        ]


class DeviceMarksFilter(django_filters.FilterSet):
    """
    Filter set for device marks data.
    """
    class Meta:
        model = DeviceMarks
        fields = [
            'id', 'title', 'description', 'code_name',
            'is_deprecated', 'creator', 'updater',
            'created_at', 'updated_at'
        ]


class DeviceModelsFilter(django_filters.FilterSet):
    """
    Filter set for device models data.
    """
    class Meta:
        model = DeviceModels
        fields = [
            'id', 'title', 'description', 'code_name',
            'is_deprecated', 'creator', 'updater',
            'created_at', 'updated_at'
        ]


class DeviceSystemsFilter(django_filters.FilterSet):
    """
    Filter set for device systems data.
    """
    class Meta:
        model = DeviceSystems
        fields = [
            'id', 'title', 'description', 'code_name',
            'is_deprecated', 'creator', 'updater',
            'created_at', 'updated_at'
        ]


class DeviceBuildsFilter(django_filters.FilterSet):
    """
    Filter set for device builds data.
    """
    class Meta:
        model = DeviceBuilds
        fields = [
            'id', 'title', 'description', 'code_name',
             'is_deprecated', 'creator', 'updater',
             'created_at', 'updated_at'
        ]


class DeviceProcessorsFilter(django_filters.FilterSet):
    """
    Filter set for device processors data.
    """
    class Meta:
        model = DeviceProcessors
        fields = [
            'id', 'title', 'description', 'code_name',
            'is_deprecated', 'creator', 'updater',
            'created_at', 'updated_at'
        ]


class DeviceRAMsFilter(django_filters.FilterSet):
    """
    Filter set for device RAMs data.
    """
    class Meta:
        model = DeviceRAMs
        fields = [
            'id', 'title', 'description', 'code_name',
            'is_deprecated', 'creator', 'updater',
            'created_at', 'updated_at'
        ]


class DeviceDisksFilter(django_filters.FilterSet):
    """
    Filter set for device disks data.
    """
    class Meta:
        model = DeviceDisks
        fields = [
            'id', 'title', 'description', 'code_name',
            'is_deprecated','creator', 'updater',
            'created_at', 'updated_at'
        ]
        

class SoftwaresFilter(django_filters.FilterSet):
    """
    Filter set for softwares data.
    """
    class Meta:
        model = Softwares
        fields = [
            'id', 'title', 'description', 'code_name',
            'is_deprecated','creator', 'updater',
            'created_at', 'updated_at'
        ]


class DeviceSoftwaresFilter(django_filters.FilterSet):
    """
    Filter set for device-softwares many-to-many relationship.
    """
    class Meta:
        model = DeviceSoftwares
        fields = [
            'id', 'device', 'software', 'installed_at'
        ]


class DevicesFilter(django_filters.FilterSet):
    """
    Filter set for devices data.
    """
    class Meta:
        model = Devices
        fields = [
            'id', 'internal_id', 'location', 'type', 'mark',
            'model', 'hostname', 'system', 'build', 'processor',
            'ram', 'disk', 'disk_internal_id', 'disk_serial',
            'network_ipv4', 'network_ipv6', 'network_mac',
            'remote_id', 'serial', 'sector', 'user_owner',
            'notes', 'creator', 'updater', 'created_at',
            'updated_at'
        ]


class NotificationTypesFilter(django_filters.FilterSet):
    """
    Filter set for notification types data.
    """
    class Meta:
        model = NotificationTypes
        fields = [
            'id', 'title', 'description', 'creator', 'updater',
            'created_at', 'updated_at'
        ]


class NotificationsFilter(django_filters.FilterSet):
    """
    Filter set for notifications data.
    """
    class Meta:
        model = Notifications
        fields = [
            'id', 'title', 'description', 'status','type', 'module',
            'module_id', 'creator', 'updater', 'created_at',
            'updated_at'
        ]
