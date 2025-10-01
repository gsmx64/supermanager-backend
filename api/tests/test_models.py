import pytest

from django.contrib.auth import get_user_model

from api.models import (
    UserProfile, LocationZones, Locations, DeviceTypes,
    DeviceMarks, DeviceModels, DeviceSystems, DeviceBuilds,
    DeviceProcessors, DeviceRAMs, DeviceDisks, Softwares,
    Devices, DeviceSoftwares, NotificationTypes,
    Notifications, AppSettings, UserSettings
)


User = get_user_model()

@pytest.mark.django_db
def test_user_profile_creation():
    user = User.objects.create_user(username='testuser', password='testpass')
    assert hasattr(user, 'profile')
    assert isinstance(user.profile, UserProfile)
    assert user.profile.user == user

@pytest.mark.django_db
def test_location_zones_creation():
    user = User.objects.create_user(username='creator', password='pass')
    zone = LocationZones.objects.create(
        title='Zone 1',
        description='Test zone',
        code_name='zone1',
        status=1,
        is_core=True,
        manager='Manager',
        manager_email='manager@example.com',
        manager_phone='123456789',
        manager_mobile='987654321',
        creator=user
    )
    assert zone.title == 'Zone 1'
    assert zone.creator == user

@pytest.mark.django_db
def test_locations_creation():
    user = User.objects.create_user(username='creator', password='pass')
    zone = LocationZones.objects.create(
        title='Zone 2',
        description='Test zone',
        code_name='zone2',
        status=1,
        is_core=True,
        manager='Manager',
        manager_email='manager@example.com',
        manager_phone='123456789',
        manager_mobile='987654321',
        creator=user
    )
    location = Locations.objects.create(
        title='Location 1',
        location_zone=zone,
        status=1,
        is_core=True,
        creator=user
    )
    assert location.title == 'Location 1'
    assert location.location_zone == zone

@pytest.mark.django_db
def test_device_types_creation():
    user = User.objects.create_user(username='creator', password='pass')
    dtype = DeviceTypes.objects.create(
        title='Laptop',
        status=1,
        is_core=True,
        creator=user
    )
    assert dtype.title == 'Laptop'
    assert dtype.creator == user

@pytest.mark.django_db
def test_device_marks_creation():
    user = User.objects.create_user(username='creator', password='pass')
    dmark = DeviceMarks.objects.create(
        title='Dell',
        status=1,
        is_core=True,
        creator=user
    )
    assert dmark.title == 'Dell'
    assert dmark.creator == user

@pytest.mark.django_db
def test_device_models_creation():
    user = User.objects.create_user(username='creator', password='pass')
    dmodel = DeviceModels.objects.create(
        title='XPS 13',
        status=1,
        is_core=True,
        creator=user
    )
    assert dmodel.title == 'XPS 13'
    assert dmodel.creator == user

@pytest.mark.django_db
def test_device_systems_creation():
    user = User.objects.create_user(username='creator', password='pass')
    dsystem = DeviceSystems.objects.create(
        title='Windows 10',
        status=1,
        is_core=True,
        creator=user
    )
    assert dsystem.title == 'Windows 10'
    assert dsystem.creator == user

@pytest.mark.django_db
def test_device_builds_creation():
    user = User.objects.create_user(username='creator', password='pass')
    dbuild = DeviceBuilds.objects.create(
        title='24H2',
        status=1,
        is_core=True,
        creator=user
    )
    assert dbuild.title == '24H2'
    assert dbuild.creator == user

@pytest.mark.django_db
def test_device_processors_creation():
    user = User.objects.create_user(username='creator', password='pass')
    dproc = DeviceProcessors.objects.create(
        title='Intel i7',
        status=1,
        is_core=True,
        creator=user
    )
    assert dproc.title == 'Intel i7'
    assert dproc.creator == user

@pytest.mark.django_db
def test_device_rams_creation():
    user = User.objects.create_user(username='creator', password='pass')
    dram = DeviceRAMs.objects.create(
        title='16GB DDR4',
        status=1,
        is_core=True,
        creator=user
    )
    assert dram.title == '16GB DDR4'
    assert dram.creator == user

@pytest.mark.django_db
def test_device_disks_creation():
    user = User.objects.create_user(username='creator', password='pass')
    disk = DeviceDisks.objects.create(
        title='1TB SSD',
        status=1,
        is_core=True,
        creator=user
    )
    assert disk.title == '1TB SSD'
    assert disk.creator == user

@pytest.mark.django_db
def test_softwares_creation():
    user = User.objects.create_user(username='creator', password='pass')
    sw = Softwares.objects.create(
        title='Windows',
        version='10',
        status=1,
        creator=user
    )
    assert sw.title == 'Windows'
    assert sw.version == '10'

@pytest.mark.django_db
def test_devices_creation_and_str():
    user = User.objects.create_user(username='creator', password='pass')
    zone = LocationZones.objects.create(
        title='Zone',
        status=1,
        is_core=True,
        creator=user
    )
    location = Locations.objects.create(
        title='Location',
        location_zone=zone,
        status=1,
        is_core=True,
        creator=user
    )
    dtype = DeviceTypes.objects.create(title='Type', status=1, is_core=True, creator=user)
    mark = DeviceMarks.objects.create(title='Mark', status=1, is_core=True, creator=user)
    model = DeviceModels.objects.create(title='Model', status=1, is_core=True, creator=user)
    system = DeviceSystems.objects.create(title='System', status=1, is_core=True, creator=user)
    build = DeviceBuilds.objects.create(title='Build', status=1, is_core=True, creator=user)
    processor = DeviceProcessors.objects.create(title='Processor', status=1, is_core=True, creator=user)
    ram = DeviceRAMs.objects.create(title='RAM', status=1, is_core=True, creator=user)
    disk = DeviceDisks.objects.create(title='Disk', status=1, is_core=True, creator=user)
    device = Devices.objects.create(
        internal_id='DEV001',
        status=1,
        location=location,
        type=dtype,
        mark=mark,
        model=model,
        hostname='host1',
        system=system,
        build=build,
        processor=processor,
        ram=ram,
        disk=disk,
        creator=user
    )
    assert device.internal_id == 'DEV001'
    assert str(device).startswith('DEV001')

@pytest.mark.django_db
def test_device_softwares_unique_together():
    user = User.objects.create_user(username='creator', password='pass')
    zone = LocationZones.objects.create(title='Zone', status=1, is_core=True, creator=user)
    location = Locations.objects.create(title='Location', location_zone=zone, status=1, is_core=True, creator=user)
    dtype = DeviceTypes.objects.create(title='Type', status=1, is_core=True, creator=user)
    mark = DeviceMarks.objects.create(title='Mark', status=1, is_core=True, creator=user)
    model = DeviceModels.objects.create(title='Model', status=1, is_core=True, creator=user)
    system = DeviceSystems.objects.create(title='System', status=1, is_core=True, creator=user)
    build = DeviceBuilds.objects.create(title='Build', status=1, is_core=True, creator=user)
    processor = DeviceProcessors.objects.create(title='Processor', status=1, is_core=True, creator=user)
    ram = DeviceRAMs.objects.create(title='RAM', status=1, is_core=True, creator=user)
    disk = DeviceDisks.objects.create(title='Disk', status=1, is_core=True, creator=user)
    device = Devices.objects.create(
        internal_id='DEV002',
        status=1,
        location=location,
        type=dtype,
        mark=mark,
        model=model,
        hostname='host2',
        system=system,
        build=build,
        processor=processor,
        ram=ram,
        disk=disk,
        creator=user
    )
    sw = Softwares.objects.create(title='Linux', version='Ubuntu', status=1, creator=user)
    ds = DeviceSoftwares.objects.create(device=device, software=sw)
    assert ds.device == device
    assert ds.software == sw
    with pytest.raises(Exception):
        DeviceSoftwares.objects.create(device=device, software=sw)

@pytest.mark.django_db
def test_notification_types_and_notifications():
    user = User.objects.create_user(username='creator', password='pass')
    ntype = NotificationTypes.objects.create(title='Type1', status=1, creator=user)
    notification = Notifications.objects.create(
        title='Notify',
        status=1,
        type=ntype,
        module='devices',
        module_id=1,
        creator=user
    )
    assert notification.title == 'Notify'
    assert notification.type == ntype

@pytest.mark.django_db
def test_app_settings_singleton():
    settings = AppSettings.objects.create()
    assert settings.number_of_alerts == 5
    assert settings.items_title_min_length == 3
    assert settings.password_min_length == 8

@pytest.mark.django_db
def test_user_settings_singleton():
    user_settings = UserSettings.objects.create()
    assert user_settings.default_language == 'en'
    assert user_settings.default_theme == 'light'
    assert user_settings.date_format_day == '2-digit'
    assert user_settings.date_format_month == '2-digit'
    assert user_settings.date_format_year == 'numeric'
    assert user_settings.time_24h == 1
    assert user_settings.timezone == 'America/New_York'
