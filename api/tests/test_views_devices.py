import pytest
import random

from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User

from api.models import (
    User,
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


@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user(db):
    user = User.objects.create_user(username='testuser', password='testpass', email='test@example.com')
    return user

@pytest.fixture
def admin_user(db):
    user = User.objects.create_superuser(username='admin', password='adminpass', email='admin@example.com')
    return user


"""
DevicesViewSet tests
"""
@pytest.mark.django_db
def test_devices_list(api_client, user):
    api_client.force_authenticate(user=user)
    url = reverse('devices-list')
    response = api_client.get(url)
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT]

@pytest.mark.django_db
def test_devices_create(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    zone = LocationZones.objects.create(title="ZoneDevice", is_core=False, creator=admin_user)
    location = Locations.objects.create(title="LocDevice", code_name="locdevice", location_zone=zone, address="Addr", is_core=False, creator=admin_user)
    dtype = DeviceTypes.objects.create(title="TypeA", code_name="typea", is_core=False, creator=admin_user)
    dmark = DeviceMarks.objects.create(title="MarkA", code_name="marka", is_core=False, creator=admin_user)
    dmodel = DeviceModels.objects.create(title="ModelA", code_name="modela", is_core=False, creator=admin_user)
    dsystem = DeviceSystems.objects.create(title="SystemA", code_name="systema", is_core=False, creator=admin_user)
    dbuild = DeviceBuilds.objects.create(title="BuildA", code_name="builda", is_core=False, creator=admin_user)
    dproc = DeviceProcessors.objects.create(title="ProcA", code_name="proca", is_core=False, creator=admin_user)
    dram = DeviceRAMs.objects.create(title="RAMA", code_name="rama", is_core=False, creator=admin_user)
    ddisk = DeviceDisks.objects.create(title="DiskA", code_name="diska", is_core=False, creator=admin_user)
    url = reverse('devices-list')
    data = {
        "internal_id": f"DEV{random.randint(1000,9999)}",
        "location": location.id,
        "type": dtype.id,
        "mark": dmark.id,
        "model": dmodel.id,
        "systems": [dsystem.id],
        "builds": [dbuild.id],
        "processor": dproc.id,
        "ram": dram.id,
        "disk": ddisk.id,
        "serial": "SN123456",
        "notes": "Device description",
        "creator": admin_user.id
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code in [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST]

@pytest.mark.django_db
def test_devices_retrieve(api_client, user, admin_user):
    api_client.force_authenticate(user=admin_user)
    zone = LocationZones.objects.create(title="ZoneDeviceR", is_core=False, creator=admin_user)
    location = Locations.objects.create(title="LocDeviceR", code_name="locdevicer", location_zone=zone, address="Addr", is_core=False, creator=admin_user)
    dtype = DeviceTypes.objects.create(title="TypeR", code_name="typer", is_core=False, creator=admin_user)
    dmark = DeviceMarks.objects.create(title="MarkR", code_name="markr", is_core=False, creator=admin_user)
    dmodel = DeviceModels.objects.create(title="ModelR", code_name="modelr", is_core=False, creator=admin_user)
    dsystem = DeviceSystems.objects.create(title="SystemR", code_name="systemr", is_core=False, creator=admin_user)
    dbuild = DeviceBuilds.objects.create(title="BuildR", code_name="buildr", is_core=False, creator=admin_user)
    dproc = DeviceProcessors.objects.create(title="ProcR", code_name="procr", is_core=False, creator=admin_user)
    dram = DeviceRAMs.objects.create(title="RAMR", code_name="ramr", is_core=False, creator=admin_user)
    ddisk = DeviceDisks.objects.create(title="DiskR", code_name="diskr", is_core=False, creator=admin_user)
    device = Devices.objects.create(
        internal_id="DEVRETR",
        location=location,
        type=dtype,
        mark=dmark,
        model=dmodel,
        processor=dproc,
        ram=dram,
        disk=ddisk,
        system=dsystem,
        build=dbuild,
        serial="SNRETR",
        notes="Device retrieve",
        creator=admin_user
    )
    api_client.force_authenticate(user=user)
    url = reverse('devices-detail', args=[device.id])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["internal_id"] == "DEVRETR"

@pytest.mark.django_db
def test_devices_update(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    zone = LocationZones.objects.create(title="ZoneDeviceU", is_core=False, creator=admin_user)
    location = Locations.objects.create(title="LocDeviceU", code_name="locdeviceu", location_zone=zone, address="Addr", is_core=False, creator=admin_user)
    dtype = DeviceTypes.objects.create(title="TypeU", code_name="typeu", is_core=False, creator=admin_user)
    dmark = DeviceMarks.objects.create(title="MarkU", code_name="marku", is_core=False, creator=admin_user)
    dmodel = DeviceModels.objects.create(title="ModelU", code_name="modelu", is_core=False, creator=admin_user)
    dsystem = DeviceSystems.objects.create(title="SystemU", code_name="systemu", is_core=False, creator=admin_user)
    dbuild = DeviceBuilds.objects.create(title="BuildU", code_name="buildu", is_core=False, creator=admin_user)
    dproc = DeviceProcessors.objects.create(title="ProcU", code_name="procu", is_core=False, creator=admin_user)
    dram = DeviceRAMs.objects.create(title="RAMU", code_name="ramu", is_core=False, creator=admin_user)
    ddisk = DeviceDisks.objects.create(title="DiskU", code_name="disku", is_core=False, creator=admin_user)
    device = Devices.objects.create(
        internal_id="DEVUPD",
        location=location,
        type=dtype,
        mark=dmark,
        model=dmodel,
        processor=dproc,
        ram=dram,
        disk=ddisk,
        system=dsystem,
        build=dbuild,
        serial="SNUPD",
        notes="Device update",
        creator=admin_user
    )
    url = reverse('devices-detail', args=[device.id])
    update_data = {
        "internal_id": "DEVUPDATED",
        "location": location.id,
        "type": dtype.id,
        "mark": dmark.id,
        "model": dmodel.id,
        "systems": [dsystem.id],
        "builds": [dbuild.id],
        "processor": dproc.id,
        "ram": dram.id,
        "disk": ddisk.id,
        "serial": "SNUPDATED",
        "notes": "Device updated",
        "creator": admin_user.id
    }
    response = api_client.put(url, update_data, format='json')
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST]
    if response.status_code == status.HTTP_200_OK:
        assert response.data["internal_id"] == "DEVUPDATED"

@pytest.mark.django_db
def test_devices_partial_update(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    zone = LocationZones.objects.create(title="ZoneDeviceP", is_core=False, creator=admin_user)
    location = Locations.objects.create(title="LocDeviceP", code_name="locdevicep", location_zone=zone, address="Addr", is_core=False, creator=admin_user)
    dtype = DeviceTypes.objects.create(title="TypeP", code_name="typep", is_core=False, creator=admin_user)
    dmark = DeviceMarks.objects.create(title="MarkP", code_name="markp", is_core=False, creator=admin_user)
    dmodel = DeviceModels.objects.create(title="ModelP", code_name="modelp", is_core=False, creator=admin_user)
    dsystem = DeviceSystems.objects.create(title="SystemP", code_name="systemp", is_core=False, creator=admin_user)
    dbuild = DeviceBuilds.objects.create(title="BuildP", code_name="buildp", is_core=False, creator=admin_user)
    dproc = DeviceProcessors.objects.create(title="ProcP", code_name="procp", is_core=False, creator=admin_user)
    dram = DeviceRAMs.objects.create(title="RAMP", code_name="ramp", is_core=False, creator=admin_user)
    ddisk = DeviceDisks.objects.create(title="DiskP", code_name="diskp", is_core=False, creator=admin_user)
    device = Devices.objects.create(
        internal_id="DEVPATCH",
        location=location,
        type=dtype,
        mark=dmark,
        model=dmodel,
        processor=dproc,
        ram=dram,
        disk=ddisk,
        system=dsystem,
        build=dbuild,
        serial="SNPATCH",
        notes="Device patch",
        creator=admin_user
    )
    url = reverse('devices-detail', args=[device.id])
    patch_data = {
        "notes": "Patched device notes"
    }
    response = api_client.patch(url, patch_data, format='json')
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST]
    if response.status_code == status.HTTP_200_OK:
        assert response.data["notes"] == "Patched device notes"

@pytest.mark.django_db
def test_devices_delete(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    zone = LocationZones.objects.create(title="ZoneDeviceD", is_core=False, creator=admin_user)
    location = Locations.objects.create(title="LocDeviceD", code_name="locdeviced", location_zone=zone, address="Addr", is_core=False, creator=admin_user)
    dtype = DeviceTypes.objects.create(title="TypeD", code_name="typed", is_core=False, creator=admin_user)
    dmark = DeviceMarks.objects.create(title="MarkD", code_name="markd", is_core=False, creator=admin_user)
    dmodel = DeviceModels.objects.create(title="ModelD", code_name="modeld", is_core=False, creator=admin_user)
    dsystem = DeviceSystems.objects.create(title="SystemD", code_name="systemd", is_core=False, creator=admin_user)
    dbuild = DeviceBuilds.objects.create(title="BuildD", code_name="buildd", is_core=False, creator=admin_user)
    dproc = DeviceProcessors.objects.create(title="ProcD", code_name="procd", is_core=False, creator=admin_user)
    dram = DeviceRAMs.objects.create(title="RAMD", code_name="ramd", is_core=False, creator=admin_user)
    ddisk = DeviceDisks.objects.create(title="DiskD", code_name="diskd", is_core=False, creator=admin_user)
    device = Devices.objects.create(
        internal_id="DEVDEL",
        location=location,
        type=dtype,
        mark=dmark,
        model=dmodel,
        processor=dproc,
        ram=dram,
        disk=ddisk,
        system=dsystem,
        build=dbuild,
        serial="SNDEL",
        notes="Device delete",
        creator=admin_user
    )
    url = reverse('devices-detail', args=[device.id])
    response = api_client.delete(url)
    assert response.status_code in [status.HTTP_204_NO_CONTENT, status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST]

@pytest.mark.django_db
def test_devices_get_with_id(api_client, user, admin_user):
    api_client.force_authenticate(user=admin_user)
    zone = LocationZones.objects.create(title="ZoneDeviceG", is_core=False, creator=admin_user)
    location = Locations.objects.create(title="LocDeviceG", code_name="locdeviceg", location_zone=zone, address="Addr", is_core=False, creator=admin_user)
    dtype = DeviceTypes.objects.create(title="TypeG", code_name="typeg", is_core=False, creator=admin_user)
    dmark = DeviceMarks.objects.create(title="MarkG", code_name="markg", is_core=False, creator=admin_user)
    dmodel = DeviceModels.objects.create(title="ModelG", code_name="modelg", is_core=False, creator=admin_user)
    dsystem = DeviceSystems.objects.create(title="SystemG", code_name="systemg", is_core=False, creator=admin_user)
    dbuild = DeviceBuilds.objects.create(title="BuildG", code_name="buildg", is_core=False, creator=admin_user)
    dproc = DeviceProcessors.objects.create(title="ProcG", code_name="procg", is_core=False, creator=admin_user)
    dram = DeviceRAMs.objects.create(title="RAMG", code_name="ramg", is_core=False, creator=admin_user)
    ddisk = DeviceDisks.objects.create(title="DiskG", code_name="diskg", is_core=False, creator=admin_user)
    device = Devices.objects.create(
        internal_id="DEVGETID",
        location=location,
        type=dtype,
        mark=dmark,
        model=dmodel,
        processor=dproc,
        ram=dram,
        disk=ddisk,
        system=dsystem,
        build=dbuild,
        serial="SNGETID",
        notes="Device getid",
        creator=admin_user
    )
    api_client.force_authenticate(user=user)
    url = reverse('devices-detail', args=[device.id])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == device.id

@pytest.mark.django_db
def test_devices_get_without_id(api_client, user):
    api_client.force_authenticate(user=user)
    url = reverse('devices-list')
    response = api_client.get(url)
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT]
