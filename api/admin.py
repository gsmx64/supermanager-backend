from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from api.models import (
    Locations, LocationZones, DeviceTypes, DeviceMarks, DeviceModels,
    DeviceSystems, DeviceBuilds, DeviceProcessors, DeviceRAMs, DeviceDisks,
    Devices, NotificationTypes, Notifications, UserProfile, User
)

class UserProfileInline(admin.StackedInline):
    """
    Inline configuration for user profile data.
    """
    model = UserProfile
    can_delete = False

class UserAdmin(BaseUserAdmin):
    """
    Admin configuration for user data.
    """
    inlines = [UserProfileInline]

"""
Admin configuration for the API application.
"""
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(UserProfile)
admin.site.register(Locations)
admin.site.register(LocationZones)
admin.site.register(DeviceTypes)
admin.site.register(DeviceMarks)
admin.site.register(DeviceModels)
admin.site.register(DeviceSystems)
admin.site.register(DeviceBuilds)
admin.site.register(DeviceProcessors)
admin.site.register(DeviceRAMs)
admin.site.register(DeviceDisks)
admin.site.register(Devices)
admin.site.register(NotificationTypes)
admin.site.register(Notifications)
admin.site.site_header = "SuperManager Admin"
