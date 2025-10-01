import pytest

from django.contrib.auth import get_user_model
from api import filters
from django.test import TestCase

from api.models import (
    UserProfile, Locations, LocationZones, DeviceTypes, DeviceMarks,
    DeviceModels, DeviceSystems, DeviceProcessors, DeviceBuilds, DeviceRAMs,
    DeviceDisks, Softwares, Devices, DeviceSoftwares, NotificationTypes, Notifications
)


User = get_user_model()

@pytest.mark.django_db
class TestFilters(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User',
            is_active=True
        )
        self.profile = self.user.profile
        self.profile.phone = '12345'
        self.profile.mobile = '54321'
        self.profile.address = '123 St'
        self.profile.city = 'TestCity'
        self.profile.state = 'TS'
        self.profile.zip_code = '00000'
        self.profile.country = 'TestLand'
        self.profile.birth = '2000-01-01'
        self.profile.title = 'Engineer'
        self.profile.about = 'About user'
        self.profile.save()
        self.location_zone = LocationZones.objects.create(
            title='Zone1',
            description='Desc',
            code_name='zone1',
            status=1,
            is_core=False,
            creator=self.user
        )
        self.location = Locations.objects.create(
            title='Loc1',
            description='Desc',
            code_name='loc1',
            status=1,
            location_zone=self.location_zone,
            is_core=False,
            sort_order=1,
            creator=self.user
        )
        self.device_type = DeviceTypes.objects.create(
            title='Type1',
            description='Desc',
            code_name='type1',
            status=1,
            is_core=False,
            sort_order=1,
            creator=self.user
        )
        self.device_mark = DeviceMarks.objects.create(
            title='Mark1',
            description='Desc',
            code_name='type1',
            status=1,
            is_core=False,
            sort_order=1,
            creator=self.user
        )
        self.device_model = DeviceModels.objects.create(
            title='Model1',
            description='Desc',
            code_name='type1',
            status=1,
            is_core=False,
            sort_order=1,
            creator=self.user
        )
        self.device_system = DeviceSystems.objects.create(
            title='System1',
            description='Desc',
            code_name='type1',
            status=1,
            is_core=False,
            sort_order=1,
            creator=self.user
        )
        self.device_build = DeviceBuilds.objects.create(
            title='Build1',
            description='Desc',
            code_name='type1',
            status=1,
            is_core=False,
            sort_order=1,
            creator=self.user
        )
        self.device_processor = DeviceProcessors.objects.create(
            title='Proc1',
            description='Desc',
            code_name='type1',
            status=1,
            is_core=False,
            sort_order=1,
            creator=self.user
        )
        self.device_ram = DeviceRAMs.objects.create(
            title='RAM1',
            description='Desc',
            code_name='type1',
            status=1,
            is_core=False,
            sort_order=1,
            creator=self.user
        )
        self.device_disk = DeviceDisks.objects.create(
            title='Disk1',
            description='Desc',
            code_name='type1',
            status=1,
            is_core=False,
            sort_order=1,
            creator=self.user
        )
        self.software = Softwares.objects.create(
            title='Soft1',
            description='Desc',
            code_name='type1',
            status=1,
            is_core=False,
            sort_order=1,
            creator=self.user
        )
        self.device = Devices.objects.create(
            internal_id='dev1',
            hostname='host1',
            location=self.location,
            type=self.device_type,
            mark=self.device_mark,
            model=self.device_model,
            system=self.device_system,
            build=self.device_build,
            processor=self.device_processor,
            ram=self.device_ram,
            disk=self.device_disk,
            status=1,
            sort_order=1,
            creator=self.user
        )
        self.device_software = DeviceSoftwares.objects.create(
            installed_at='2024-01-01 00:00:00.000000',
            device=self.device,
            software=self.software
        )
        self.notification_type = NotificationTypes.objects.create(
            title='NotifType1',
            description='Desc',
            status=1,
            is_core=False,
            sort_order=1,
            creator=self.user
        )
        self.notification = Notifications.objects.create(
            title='Notif1',
            description='Desc',
            status=1,
            type=self.notification_type,
            module='module1/submodule',
            module_id=1,
            creator=self.user
        )

    def test_user_extended_filter(self):
        qs = User.objects.all()
        f = filters.UserExtendedFilter({'profile__phone': '123'}, queryset=qs)
        assert self.user in f.qs

    def test_users_filter(self):
        qs = User.objects.all()
        f = filters.UsersFilter({'username': 'testuser'}, queryset=qs)
        assert self.user in f.qs

    def test_users_profile_filter(self):
        qs = UserProfile.objects.all()
        f = filters.UsersProfileFilter({'phone': '12345'}, queryset=qs)
        assert self.profile in f.qs

    def test_location_zones_filter(self):
        qs = LocationZones.objects.all()
        f = filters.LocationZonesFilter({'title': 'Zone1'}, queryset=qs)
        assert self.location_zone in f.qs

    def test_locations_filter(self):
        qs = Locations.objects.all()
        f = filters.LocationsFilter({'title': 'Loc1'}, queryset=qs)
        assert self.location in f.qs

    def test_device_types_filter(self):
        qs = DeviceTypes.objects.all()
        f = filters.DeviceTypesFilter({'title': 'Type1'}, queryset=qs)
        assert self.device_type in f.qs

    def test_device_marks_filter(self):
        qs = DeviceMarks.objects.all()
        f = filters.DeviceMarksFilter({'title': 'Mark1'}, queryset=qs)
        assert self.device_mark in f.qs

    def test_device_models_filter(self):
        qs = DeviceModels.objects.all()
        f = filters.DeviceModelsFilter({'title': 'Model1'}, queryset=qs)
        assert self.device_model in f.qs

    def test_device_systems_filter(self):
        qs = DeviceSystems.objects.all()
        f = filters.DeviceSystemsFilter({'title': 'System1'}, queryset=qs)
        assert self.device_system in f.qs

    def test_device_builds_filter(self):
        qs = DeviceBuilds.objects.all()
        f = filters.DeviceBuildsFilter({'title': 'Build1'}, queryset=qs)
        assert self.device_build in f.qs

    def test_device_processors_filter(self):
        qs = DeviceProcessors.objects.all()
        f = filters.DeviceProcessorsFilter({'title': 'Proc1'}, queryset=qs)
        assert self.device_processor in f.qs

    def test_device_rams_filter(self):
        qs = DeviceRAMs.objects.all()
        f = filters.DeviceRAMsFilter({'title': 'RAM1'}, queryset=qs)
        assert self.device_ram in f.qs

    def test_device_disks_filter(self):
        qs = DeviceDisks.objects.all()
        f = filters.DeviceDisksFilter({'title': 'Disk1'}, queryset=qs)
        assert self.device_disk in f.qs

    def test_softwares_filter(self):
        qs = Softwares.objects.all()
        f = filters.SoftwaresFilter({'title': 'Soft1'}, queryset=qs)
        assert self.software in f.qs

    def test_device_softwares_filter(self):
        qs = DeviceSoftwares.objects.all()
        f = filters.DeviceSoftwaresFilter({'device': self.device.id}, queryset=qs)
        assert self.device_software in f.qs

    def test_devices_filter(self):
        qs = Devices.objects.all()
        f = filters.DevicesFilter({'internal_id': 'dev1'}, queryset=qs)
        assert self.device in f.qs

    def test_notification_types_filter(self):
        qs = NotificationTypes.objects.all()
        f = filters.NotificationTypesFilter({'title': 'NotifType1'}, queryset=qs)
        assert self.notification_type in f.qs

    def test_notifications_filter(self):
        qs = Notifications.objects.all()
        f = filters.NotificationsFilter({'title': 'Notif1'}, queryset=qs)
        assert self.notification in f.qs
