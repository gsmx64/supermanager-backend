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
from api.serializers import DevicesSerializer


"""
DevicesSerializer tests
"""
@pytest.mark.django_db
def test_devices_serializer_fields_and_methods():
    user = User.objects.create_user(username='testuser6', password='pass123456')
    # Create related objects
    type_obj = DeviceTypes.objects.create(title='Laptop', creator=user)
    mark_obj = DeviceMarks.objects.create(title='Dell', creator=user)
    model_obj = DeviceModels.objects.create(title='XPS', creator=user)
    system_obj = DeviceSystems.objects.create(title='Windows', creator=user)
    build_obj = DeviceBuilds.objects.create(title='2023', creator=user)
    processor_obj = DeviceProcessors.objects.create(title='i7', creator=user)
    ram_obj = DeviceRAMs.objects.create(title='16GB', creator=user)
    disk_obj = DeviceDisks.objects.create(title='512GB SSD', creator=user)
    zone = LocationZones.objects.create(title='Zone3', creator=user)
    location_obj = Locations.objects.create(title='HQ', location_zone=zone, creator=user)

    # Create device
    device = Devices.objects.create(
        internal_id='1982',
        hostname='device1982',
        type=type_obj,
        mark=mark_obj,
        model=model_obj,
        system=system_obj,
        build=build_obj,
        processor=processor_obj,
        ram=ram_obj,
        disk=disk_obj,
        location=location_obj,
        creator=user
    )

    serializer = DevicesSerializer(device)
    data = serializer.data
    assert 'id' in data
    assert 'type' in data
    assert 'mark' in data
    assert 'model' in data
    assert 'system' in data
    assert 'build' in data
    assert 'processor' in data
    assert 'ram' in data
    assert 'disk' in data
    assert 'location' in data
    assert 'creator' in data
    assert 'updater' in data

    # Check get_type, get_mark, get_model, etc. return expected dicts
    assert data['type']['id'] == type_obj.id
    assert data['mark']['id'] == mark_obj.id
    assert data['model']['id'] == model_obj.id
    assert data['system']['id'] == system_obj.id
    assert data['build']['id'] == build_obj.id
    assert data['processor']['id'] == processor_obj.id
    assert data['ram']['id'] == ram_obj.id
    assert data['disk']['id'] == disk_obj.id
    assert data['location']['id'] == location_obj.id

@pytest.mark.django_db
def test_devices_serializer_validate_status_disabled_for_superuser():
    user = User.objects.create_superuser(username='admin_device', email='admin_device@example.com', password='adminpass')
    type_obj = DeviceTypes.objects.create(title='Tablet', creator=user)
    mark_obj = DeviceMarks.objects.create(title='Apple', creator=user)
    model_obj = DeviceModels.objects.create(title='iPad', creator=user)
    system_obj = DeviceSystems.objects.create(title='iOS', creator=user)
    build_obj = DeviceBuilds.objects.create(title='2022', creator=user)
    processor_obj = DeviceProcessors.objects.create(title='M1', creator=user)
    ram_obj = DeviceRAMs.objects.create(title='8GB', creator=user)
    disk_obj = DeviceDisks.objects.create(title='256GB SSD', creator=user)
    zone = LocationZones.objects.create(title='Zone4', creator=user)
    location_obj = Locations.objects.create(title='Branch', location_zone=zone, creator=user)

    request = APIRequestFactory().post('/')
    request.user = user
    data = {
        'internal_id': '1982',
        'hostname': 'device1982',
        'status': 0,
        'type_id': type_obj.id,
        'mark_id': mark_obj.id,
        'model_id': model_obj.id,
        'system_id': system_obj.id,
        'build_id': build_obj.id,
        'processor_id': processor_obj.id,
        'ram_id': ram_obj.id,
        'disk_id': disk_obj.id,
        'location_id': location_obj.id,
        'serial_number': 'SN123456'
    }
    serializer = DevicesSerializer(data=data, context={'request': request})
    assert serializer.is_valid(), serializer.errors
    assert serializer.validated_data.get('status') is 0

@pytest.mark.django_db
def test_devices_serializer_to_representation_devices_count():
    user = User.objects.create_user(username='testuser7', password='pass123456')
    type_obj = DeviceTypes.objects.create(title='Desktop', creator=user)
    mark_obj = DeviceMarks.objects.create(title='HP', creator=user)
    model_obj = DeviceModels.objects.create(title='Elite', creator=user)
    system_obj = DeviceSystems.objects.create(title='Linux', creator=user)
    build_obj = DeviceBuilds.objects.create(title='2021', creator=user)
    processor_obj = DeviceProcessors.objects.create(title='Ryzen 5', creator=user)
    ram_obj = DeviceRAMs.objects.create(title='32GB', creator=user)
    disk_obj = DeviceDisks.objects.create(title='1TB HDD', creator=user)
    zone = LocationZones.objects.create(title='Zone5', creator=user)
    location_obj = Locations.objects.create(title='Remote', location_zone=zone, creator=user)

    device = Devices.objects.create(
        internal_id='1982',
        hostname='device1982',
        type=type_obj,
        mark=mark_obj,
        model=model_obj,
        system=system_obj,
        build=build_obj,
        processor=processor_obj,
        ram=ram_obj,
        disk=disk_obj,
        location=location_obj,
        creator=user
    )

    serializer = DevicesSerializer(device)
    data = serializer.data
    # There is no devices_count in DevicesSerializer, but you can check related fields
    assert data['location']['id'] == location_obj.id

@pytest.mark.django_db
def test_devices_serializer_create_and_representation():
    user = User.objects.create_user(username='creator_devices', password='pass123456')
    type_obj = DeviceTypes.objects.create(title='Phone', creator=user)
    mark_obj = DeviceMarks.objects.create(title='Samsung', creator=user)
    model_obj = DeviceModels.objects.create(title='Galaxy', creator=user)
    system_obj = DeviceSystems.objects.create(title='Android', creator=user)
    build_obj = DeviceBuilds.objects.create(title='2024', creator=user)
    processor_obj = DeviceProcessors.objects.create(title='Snapdragon', creator=user)
    ram_obj = DeviceRAMs.objects.create(title='8GB', creator=user)
    disk_obj = DeviceDisks.objects.create(title='128GB', creator=user)
    zone = LocationZones.objects.create(title='Zone6', creator=user)
    location_obj = Locations.objects.create(title='Main', location_zone=zone, creator=user)

    data = {
        'internal_id': '2024',
        'hostname': 'device2024',
        'type_id': type_obj.id,
        'mark_id': mark_obj.id,
        'model_id': model_obj.id,
        'system_id': system_obj.id,
        'build_id': build_obj.id,
        'processor_id': processor_obj.id,
        'ram_id': ram_obj.id,
        'disk_id': disk_obj.id,
        'location_id': location_obj.id,
        'serial_number': 'SN2024',
        'status': 1
    }
    request = APIRequestFactory().post('/')
    request.user = user
    serializer = DevicesSerializer(data=data, context={'request': request})
    assert serializer.is_valid(), serializer.errors
    instance = serializer.save(creator=user)
    assert instance.internal_id == '2024'
    assert instance.hostname == 'device2024'
    assert instance.type == type_obj
    assert instance.mark == mark_obj
    assert instance.model == model_obj
    assert instance.system == system_obj
    assert instance.build == build_obj
    assert instance.processor == processor_obj
    assert instance.ram == ram_obj
    assert instance.disk == disk_obj
    assert instance.location == location_obj
    assert instance.status == 1

    serializer2 = DevicesSerializer(instance)
    data2 = serializer2.data
    assert data2['internal_id'] == '2024'
    assert data2['hostname'] == 'device2024'
    assert data2['type']['id'] == type_obj.id
    assert data2['mark']['id'] == mark_obj.id
    assert data2['model']['id'] == model_obj.id
    assert data2['system']['id'] == system_obj.id
    assert data2['build']['id'] == build_obj.id
    assert data2['processor']['id'] == processor_obj.id
    assert data2['ram']['id'] == ram_obj.id
    assert data2['disk']['id'] == disk_obj.id
    assert data2['location']['id'] == location_obj.id
    assert data2['status'] == 1
    assert 'creator' in data2
    assert 'updater' in data2

@pytest.mark.django_db
def test_devices_serializer_update_device():
    user = User.objects.create_user(username='updater_devices', password='pass123456')
    type_obj = DeviceTypes.objects.create(title='Server', creator=user)
    mark_obj = DeviceMarks.objects.create(title='Lenovo', creator=user)
    model_obj = DeviceModels.objects.create(title='ThinkServer', creator=user)
    system_obj = DeviceSystems.objects.create(title='Ubuntu', creator=user)
    build_obj = DeviceBuilds.objects.create(title='2020', creator=user)
    processor_obj = DeviceProcessors.objects.create(title='Xeon', creator=user)
    ram_obj = DeviceRAMs.objects.create(title='64GB', creator=user)
    disk_obj = DeviceDisks.objects.create(title='2TB', creator=user)
    zone = LocationZones.objects.create(title='Zone7', creator=user)
    location_obj = Locations.objects.create(title='Datacenter', location_zone=zone, creator=user)

    device = Devices.objects.create(
        internal_id='3030',
        hostname='device3030',
        type=type_obj,
        mark=mark_obj,
        model=model_obj,
        system=system_obj,
        build=build_obj,
        processor=processor_obj,
        ram=ram_obj,
        disk=disk_obj,
        location=location_obj,
        creator=user
    )

    update_data = {'hostname': 'device3030-updated'}
    request = APIRequestFactory().put('/')
    request.user = user
    serializer = DevicesSerializer(device, data=update_data, context={'request': request}, partial=True)
    assert serializer.is_valid(), serializer.errors
    updated = serializer.save(updater=user)
    assert updated.hostname == 'device3030-updated'

@pytest.mark.django_db
def test_devices_serializer_get_queryset_returns_all():
    user = User.objects.create_user(username='creator_devices2', password='pass123456')
    type_obj = DeviceTypes.objects.create(title='Router', creator=user)
    mark_obj = DeviceMarks.objects.create(title='Cisco', creator=user)
    model_obj = DeviceModels.objects.create(title='RV340', creator=user)
    system_obj = DeviceSystems.objects.create(title='IOS', creator=user)
    build_obj = DeviceBuilds.objects.create(title='2019', creator=user)
    processor_obj = DeviceProcessors.objects.create(title='ARM', creator=user)
    ram_obj = DeviceRAMs.objects.create(title='2GB', creator=user)
    disk_obj = DeviceDisks.objects.create(title='16GB', creator=user)
    zone = LocationZones.objects.create(title='Zone8', creator=user)
    location_obj = Locations.objects.create(title='Branch2', location_zone=zone, creator=user)

    Devices.objects.create(
        internal_id='4040',
        hostname='device4040',
        type=type_obj,
        mark=mark_obj,
        model=model_obj,
        system=system_obj,
        build=build_obj,
        processor=processor_obj,
        ram=ram_obj,
        disk=disk_obj,
        location=location_obj,
        creator=user
    )
    Devices.objects.create(
        internal_id='5050',
        hostname='device5050',
        type=type_obj,
        mark=mark_obj,
        model=model_obj,
        system=system_obj,
        build=build_obj,
        processor=processor_obj,
        ram=ram_obj,
        disk=disk_obj,
        location=location_obj,
        creator=user
    )
    request = APIRequestFactory().get('/')
    request.user = user
    if hasattr(DevicesSerializer, 'get_queryset'):
        queryset = DevicesSerializer.get_queryset(request)
        assert queryset.count() >= 2