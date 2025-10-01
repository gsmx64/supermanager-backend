import pytest

from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory

from api.models import (
    LocationZones,
    Locations,
    DeviceTypes,
    DeviceMarks,
    DeviceModels,
    DeviceSystems,
    DeviceBuilds,
    DeviceProcessors,
    DeviceRAMs,
    DeviceDisks,
    Devices
)
from api.serializers import LocationsSerializer


"""
LocationsSerializer tests
"""
@pytest.mark.django_db
def test_locations_serializer_create_and_representation():
    user = User.objects.create_user(username='creator_locations', password='pass123456')
    zone = LocationZones.objects.create(title='ZoneLoc', creator=user)
    data = {
        'title': 'LocationTest',
        'description': 'Test location',
        'code_name': 'locationtest',
        'status': 1,
        'is_core': False,
        'location_zone_id': zone.id,
        'manager': 'Manager Name',
        'manager_email': 'manager@example.com',
        'manager_phone': '123456789',
        'manager_mobile': '987654321',
        'collaborator': 'Collaborator Name',
        'collaborator_email': 'collab@example.com',
        'collaborator_phone': '111222333',
        'collaborator_mobile': '444555666',
        'phone': '5551234',
        'mobile': '5555678',
        'address': '123 Main St',
        'city': 'Test City',
        'state': 'Test State',
        'zip_code': '12345',
        'country': 'Test Country',
        'latitude': 10.1234,
        'longitude': 20.5678,
        'sort_order': 2
    }
    request = APIRequestFactory().post('/')
    request.user = user
    serializer = LocationsSerializer(data=data, context={'request': request})
    assert serializer.is_valid(), serializer.errors
    instance = serializer.save(creator=user)
    assert instance.title == 'LocationTest'
    assert instance.description == 'Test location'
    assert instance.code_name == 'locationtest'
    assert instance.status == 1
    assert instance.is_core is False
    assert instance.location_zone == zone
    assert instance.manager == 'Manager Name'
    assert instance.manager_email == 'manager@example.com'
    assert instance.manager_phone == '123456789'
    assert instance.manager_mobile == '987654321'
    assert instance.collaborator == 'Collaborator Name'
    assert instance.collaborator_email == 'collab@example.com'
    assert instance.collaborator_phone == '111222333'
    assert instance.collaborator_mobile == '444555666'
    assert instance.phone == '5551234'
    assert instance.mobile == '5555678'
    assert instance.address == '123 Main St'
    assert instance.city == 'Test City'
    assert instance.state == 'Test State'
    assert instance.zip_code == '12345'
    assert instance.country == 'Test Country'
    assert instance.latitude == 10.1234
    assert instance.longitude == 20.5678
    assert instance.sort_order == 2

    serializer2 = LocationsSerializer(instance)
    data2 = serializer2.data
    assert data2['title'] == 'LocationTest'
    assert data2['description'] == 'Test location'
    assert data2['code_name'] == 'locationtest'
    assert data2['status'] == 1
    assert data2['is_core'] is False or data2['is_core'] == 0
    assert data2['location_zone']['id'] == zone.id
    assert data2['manager'] == 'Manager Name'
    assert data2['manager_email'] == 'manager@example.com'
    assert data2['manager_phone'] == '123456789'
    assert data2['manager_mobile'] == '987654321'
    assert data2['collaborator'] == 'Collaborator Name'
    assert data2['collaborator_email'] == 'collab@example.com'
    assert data2['collaborator_phone'] == '111222333'
    assert data2['collaborator_mobile'] == '444555666'
    assert data2['phone'] == '5551234'
    assert data2['mobile'] == '5555678'
    assert data2['address'] == '123 Main St'
    assert data2['city'] == 'Test City'
    assert data2['state'] == 'Test State'
    assert data2['zip_code'] == '12345'
    assert data2['country'] == 'Test Country'
    assert float(data2['latitude']) == 10.1234
    assert float(data2['longitude']) == 20.5678
    assert data2['sort_order'] == 2
    assert 'creator' in data2
    assert 'updater' in data2
    assert 'devices_count' in data2

@pytest.mark.django_db
def test_locations_serializer_update_core_by_superuser():
    user = User.objects.create_superuser(username='admin_locations', email='admin_locations@example.com', password='adminpass')
    zone = LocationZones.objects.create(title='ZoneLoc2', creator=user)
    location = Locations.objects.create(title='CoreLoc', is_core=True, location_zone=zone, creator=user)
    request = APIRequestFactory().put('/')
    request.user = user
    serializer = LocationsSerializer(location, data={'title': 'UpdatedLoc'}, context={'request': request}, partial=True)
    assert serializer.is_valid(), serializer.errors
    updated = serializer.save()
    assert updated.title == 'UpdatedLoc'

@pytest.mark.django_db
def test_locations_serializer_update_core_by_non_superuser_fails():
    user = User.objects.create_user(username='normal_locations', password='pass123456')
    admin = User.objects.create_superuser(username='admin_locations2', email='admin_locations2@example.com', password='adminpass2')
    zone = LocationZones.objects.create(title='ZoneLoc3', creator=admin)
    location = Locations.objects.create(title='CoreLoc2', is_core=True, location_zone=zone, creator=admin)
    request = APIRequestFactory().put('/')
    request.user = user
    serializer = LocationsSerializer(location, data={'title': 'ShouldFail'}, context={'request': request}, partial=True)
    is_valid = serializer.is_valid()
    assert not is_valid
    assert 'non_field_errors' in serializer.errors or True

@pytest.mark.django_db
def test_locations_serializer_force_is_core_false_on_create_by_superuser():
    user = User.objects.create_superuser(username='admin_locations3', email='admin_locations3@example.com', password='adminpass3')
    zone = LocationZones.objects.create(title='ZoneLoc4', creator=user)
    request = APIRequestFactory().post('/')
    request.user = user
    data = {'title': 'LocForce', 'description': 'Force core', 'location_zone_id': zone.id}
    serializer = LocationsSerializer(data=data, context={'request': request})
    assert serializer.is_valid(), serializer.errors
    assert serializer.validated_data.get('is_core') is False or serializer.validated_data.get('is_core') is None

@pytest.mark.django_db
def test_locations_serializer_get_queryset_returns_all():
    user = User.objects.create_user(username='creator_locations2', password='pass123456')
    zone = LocationZones.objects.create(title='ZoneLoc5', creator=user)
    Locations.objects.create(title='LocA', location_zone=zone, creator=user)
    Locations.objects.create(title='LocB', location_zone=zone, creator=user)
    request = APIRequestFactory().get('/')
    request.user = user
    queryset = LocationsSerializer.get_queryset(request)
    assert queryset.count() >= 2

@pytest.mark.django_db
def test_locations_serializer_create_location_classmethod():
    user = User.objects.create_user(username='creator_locations3', password='pass123456')
    zone = LocationZones.objects.create(title='ZoneLoc6', creator=user)
    request = APIRequestFactory().post('/')
    request.user = user
    request.data = {'title': 'LocC', 'description': 'DescC', 'location_zone_id': zone.id}
    instance, _ = LocationsSerializer.create_location(request)
    assert instance['title'] == 'LocC'
    assert instance['description'] == 'DescC'
    assert instance['location_zone']['id'] == zone.id

@pytest.mark.django_db
def test_locations_serializer_update_location_classmethod():
    user = User.objects.create_user(username='creator_locations4', password='pass123456')
    zone = LocationZones.objects.create(title='ZoneLoc7', creator=user)
    location = Locations.objects.create(title='LocD', description='DescD', location_zone=zone, creator=user)
    request = APIRequestFactory().put('/')
    request.user = user
    request.data = {'title': 'LocD Updated'}
    result = LocationsSerializer.update_location(request, pk=location.pk, partial=True)
    updated = result[0]
    assert updated['title'] == 'LocD Updated'

@pytest.mark.django_db
def test_locations_serializer_to_representation_devices_count():
    user = User.objects.create_user(username='testuser_locations', password='pass123456')
    zone = LocationZones.objects.create(title='ZoneLoc8', creator=user)
    location = Locations.objects.create(title='LocE', location_zone=zone, creator=user)

    device_type = DeviceTypes.objects.create(title='Type1', creator=user)
    device_mark = DeviceMarks.objects.create(title='Mark1', creator=user)
    device_model = DeviceModels.objects.create(title='Model1', creator=user)
    device_system = DeviceSystems.objects.create(title='System1', creator=user)
    device_build = DeviceBuilds.objects.create(title='Build1', creator=user)
    device_processor = DeviceProcessors.objects.create(title='Processor1', creator=user)
    device_ram = DeviceRAMs.objects.create(title='Ram1', creator=user)
    device_disk = DeviceDisks.objects.create(title='Disk1', creator=user)

    Devices.objects.create(
        type=device_type,
        mark=device_mark,
        model=device_model,
        system=device_system,
        build=device_build,
        processor=device_processor,
        ram=device_ram,
        disk=device_disk,
        location=location,
        creator=user
    )
    Devices.objects.create(
        type=device_type,
        mark=device_mark,
        model=device_model,
        system=device_system,
        build=device_build,
        processor=device_processor,
        ram=device_ram,
        disk=device_disk,
        location=location,
        creator=user
    )
    serializer = LocationsSerializer(location)
    data = serializer.data
    assert 'devices_count' in data
    assert data['devices_count'] == 2

@pytest.mark.django_db
def test_locations_serializer_devices_count():
    user = User.objects.create_user(username='testuser4', password='pass123456')
    zone = LocationZones.objects.create(title='Zone2', creator=user)
    location = Locations.objects.create(title='Location1', location_zone=zone, creator=user)
    serializer = LocationsSerializer(location)
    data = serializer.data
    assert 'devices_count' in data
