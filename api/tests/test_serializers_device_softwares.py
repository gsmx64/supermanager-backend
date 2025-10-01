import pytest
import datetime

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
    Softwares,
    Devices,
    DeviceSoftwares
)
from api.serializers import DeviceSoftwaresSerializer


"""
DeviceSoftwaresSerializer tests
"""
@pytest.mark.django_db
def test_device_softwares_serializer_create_and_representation():
    user = User.objects.create_user(username='creator_softdev', password='pass123456')
    type_obj = DeviceTypes.objects.create(title='PC', creator=user)
    mark_obj = DeviceMarks.objects.create(title='Lenovo', creator=user)
    model_obj = DeviceModels.objects.create(title='ThinkPad', creator=user)
    system_obj = DeviceSystems.objects.create(title='Ubuntu', creator=user)
    build_obj = DeviceBuilds.objects.create(title='2024', creator=user)
    processor_obj = DeviceProcessors.objects.create(title='i5', creator=user)
    ram_obj = DeviceRAMs.objects.create(title='8GB', creator=user)
    disk_obj = DeviceDisks.objects.create(title='256GB SSD', creator=user)
    zone = LocationZones.objects.create(title='ZoneSoft', creator=user)
    location_obj = Locations.objects.create(title='Office', location_zone=zone, creator=user)
    device = Devices.objects.create(
        type=type_obj, mark=mark_obj, model=model_obj, system=system_obj, build=build_obj,
        processor=processor_obj, ram=ram_obj, disk=disk_obj, location=location_obj, creator=user
    )
    software = Softwares.objects.create(title='Antivirus', creator=user)
    data = {
        'device': device.id,
        'software': software.id
    }
    serializer = DeviceSoftwaresSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    instance = serializer.save()
    assert instance.device == device
    assert instance.software == software

    serializer2 = DeviceSoftwaresSerializer(instance)
    data2 = serializer2.data
    assert 'id' in data2
    assert 'device' in data2  # device is included in the serializer output
    assert 'software' in data2
    assert data2['software'] == software.id

@pytest.mark.django_db
def test_device_softwares_serializer_to_representation():
    user = User.objects.create_user(username='creator_softdev2', password='pass123456')
    type_obj = DeviceTypes.objects.create(title='PC', creator=user)
    mark_obj = DeviceMarks.objects.create(title='Acer', creator=user)
    model_obj = DeviceModels.objects.create(title='Aspire', creator=user)
    system_obj = DeviceSystems.objects.create(title='Windows', creator=user)
    build_obj = DeviceBuilds.objects.create(title='2022', creator=user)
    processor_obj = DeviceProcessors.objects.create(title='i3', creator=user)
    ram_obj = DeviceRAMs.objects.create(title='4GB', creator=user)
    disk_obj = DeviceDisks.objects.create(title='128GB SSD', creator=user)
    zone = LocationZones.objects.create(title='ZoneSoft2', creator=user)
    location_obj = Locations.objects.create(title='Lab', location_zone=zone, creator=user)
    device = Devices.objects.create(
        type=type_obj, mark=mark_obj, model=model_obj, system=system_obj, build=build_obj,
        processor=processor_obj, ram=ram_obj, disk=disk_obj, location=location_obj, creator=user
    )
    software = Softwares.objects.create(title='Office', creator=user)
    dev_soft = DeviceSoftwares.objects.create(device=device, software=software)
    serializer = DeviceSoftwaresSerializer(dev_soft)
    data = serializer.data
    assert 'id' in data
    assert 'software' in data
    assert data['software'] == software.id

@pytest.mark.django_db
def test_device_softwares_serializer_get_queryset_returns_all():
    user = User.objects.create_user(username='creator_softdev3', password='pass123456')
    type_obj = DeviceTypes.objects.create(title='Tablet', creator=user)
    mark_obj = DeviceMarks.objects.create(title='Samsung', creator=user)
    model_obj = DeviceModels.objects.create(title='Tab', creator=user)
    system_obj = DeviceSystems.objects.create(title='Android', creator=user)
    build_obj = DeviceBuilds.objects.create(title='2021', creator=user)
    processor_obj = DeviceProcessors.objects.create(title='Snapdragon', creator=user)
    ram_obj = DeviceRAMs.objects.create(title='6GB', creator=user)
    disk_obj = DeviceDisks.objects.create(title='64GB', creator=user)
    zone = LocationZones.objects.create(title='ZoneSoft3', creator=user)
    location_obj = Locations.objects.create(title='Mobile', location_zone=zone, creator=user)
    device = Devices.objects.create(
        type=type_obj, mark=mark_obj, model=model_obj, system=system_obj, build=build_obj,
        processor=processor_obj, ram=ram_obj, disk=disk_obj, location=location_obj, creator=user
    )
    software1 = Softwares.objects.create(title='App1', creator=user)
    software2 = Softwares.objects.create(title='App2', creator=user)
    DeviceSoftwares.objects.create(device=device, software=software1)
    DeviceSoftwares.objects.create(device=device, software=software2)
    request = APIRequestFactory().get('/')
    request.user = user
    queryset = DeviceSoftwaresSerializer.get_queryset(request)
    assert queryset.count() >= 2

@pytest.mark.django_db
def test_device_softwares_serializer_create_device_software_classmethod():
    user = User.objects.create_user(username='creator_softdev4', password='pass123456')
    type_obj = DeviceTypes.objects.create(title='Server', creator=user)
    mark_obj = DeviceMarks.objects.create(title='IBM', creator=user)
    model_obj = DeviceModels.objects.create(title='Power', creator=user)
    system_obj = DeviceSystems.objects.create(title='AIX', creator=user)
    build_obj = DeviceBuilds.objects.create(title='2020', creator=user)
    processor_obj = DeviceProcessors.objects.create(title='Power9', creator=user)
    ram_obj = DeviceRAMs.objects.create(title='128GB', creator=user)
    disk_obj = DeviceDisks.objects.create(title='2TB HDD', creator=user)
    zone = LocationZones.objects.create(title='ZoneSoft4', creator=user)
    location_obj = Locations.objects.create(title='Datacenter', location_zone=zone, creator=user)
    device = Devices.objects.create(
        type=type_obj, mark=mark_obj, model=model_obj, system=system_obj, build=build_obj,
        processor=processor_obj, ram=ram_obj, disk=disk_obj, location=location_obj, creator=user
    )
    software = Softwares.objects.create(title='DBMS', creator=user)
    request = APIRequestFactory().post('/')
    request.user = user
    request.data = {'device_id': device.id, 'software_id': software.id}
    instance = DeviceSoftwaresSerializer.create_device_software(request)
    assert instance.device == device
    assert instance.software == software

@pytest.mark.django_db
def test_device_softwares_serializer_update_device_software_classmethod():
    user = User.objects.create_user(username='creator_softdev5', password='pass123456')
    type_obj = DeviceTypes.objects.create(title='Router', creator=user)
    mark_obj = DeviceMarks.objects.create(title='Cisco', creator=user)
    model_obj = DeviceModels.objects.create(title='RV340', creator=user)
    system_obj = DeviceSystems.objects.create(title='IOS', creator=user)
    build_obj = DeviceBuilds.objects.create(title='2019', creator=user)
    processor_obj = DeviceProcessors.objects.create(title='ARM', creator=user)
    ram_obj = DeviceRAMs.objects.create(title='2GB', creator=user)
    disk_obj = DeviceDisks.objects.create(title='16GB', creator=user)
    zone = LocationZones.objects.create(title='ZoneSoft5', creator=user)
    location_obj = Locations.objects.create(title='Network', location_zone=zone, creator=user)
    device = Devices.objects.create(
        type=type_obj, mark=mark_obj, model=model_obj, system=system_obj, build=build_obj,
        processor=processor_obj, ram=ram_obj, disk=disk_obj, location=location_obj, creator=user
    )
    software = Softwares.objects.create(title='Firmware', creator=user)
    dev_soft = DeviceSoftwares.objects.create(device=device, software=software)
    new_software = Softwares.objects.create(title='Firmware v2', creator=user)
    request = APIRequestFactory().put('/')
    request.user = user
    request.data = {'software_id': new_software.id}
    updated = DeviceSoftwaresSerializer.update_device_software(request, pk=dev_soft.pk, partial=True)
    assert updated.software == new_software
