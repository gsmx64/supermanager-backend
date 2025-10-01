from rest_framework import routers

from api.views import (
    AuthCustomViewSet, UserExtendedViewSet, UserProfileViewSet,
    LocationsViewSet, LocationZonesViewSet, DeviceTypesViewSet,
    DeviceMarksViewSet, DeviceModelsViewSet, DeviceSystemsViewSet,
    DeviceBuildsViewSet, DeviceProcessorsViewSet, DeviceRAMsViewSet,
    DeviceDisksViewSet, SoftwaresViewSet, DevicesViewSet,
    NotificationTypesViewSet, DeviceSoftwaresViewSet,
    NotificationsViewSet, AppSettingsViewSet, UserSettingsViewSet
)

"""
API URL Configuration
"""
router = routers.DefaultRouter()
router.register(r'auth', AuthCustomViewSet, basename='auth')
router.register(r'users', UserExtendedViewSet, basename='users')
router.register(r'profile', UserProfileViewSet, basename='profile')
router.register(r'locations', LocationsViewSet, basename='locations')
router.register(r'location-zones', LocationZonesViewSet, basename='location-zones')
router.register(r'device-types', DeviceTypesViewSet, basename='device-types')
router.register(r'device-marks', DeviceMarksViewSet, basename='device-marks')
router.register(r'device-models', DeviceModelsViewSet, basename='device-models')
router.register(r'device-systems', DeviceSystemsViewSet, basename='device-systems')
router.register(r'device-builds', DeviceBuildsViewSet, basename='device-builds')
router.register(r'device-processors', DeviceProcessorsViewSet, basename='device-processors')
router.register(r'device-rams', DeviceRAMsViewSet, basename='device-rams')
router.register(r'device-disks', DeviceDisksViewSet, basename='device-disks')
router.register(r'softwares', SoftwaresViewSet, basename='softwares')
router.register(r'devices', DevicesViewSet, basename='devices')
router.register(r'device-softwares', DeviceSoftwaresViewSet, basename='device-softwares')
router.register(r'notification-types', NotificationTypesViewSet, basename='notification-types')
router.register(r'notifications', NotificationsViewSet, basename='notifications')
router.register(r'app-settings', AppSettingsViewSet, basename='app-settings')
router.register(r'user-settings', UserSettingsViewSet, basename='user-settings')

urlpatterns = router.urls
