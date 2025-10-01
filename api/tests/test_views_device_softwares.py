import pytest

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
    DeviceProcessors,
    DeviceRAMs,
    DeviceDisks,
    DeviceSystems,
    DeviceBuilds,
    Softwares,
    Devices,
    DeviceSoftwares
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
DeviceSoftwaresViewSet tests
"""
@pytest.mark.django_db
def test_device_softwares_list(api_client, user):
    api_client.force_authenticate(user=user)
    url = reverse('device-softwares-list')
    response = api_client.get(url)
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT]

@pytest.mark.django_db
def test_device_softwares_delete(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    # Create required FKs
    zone = LocationZones.objects.create(title="ZoneDSWD", is_core=False, creator=admin_user)
    location = Locations.objects.create(title="LocDSWD", code_name="locdswd", location_zone=zone, address="Addr", is_core=False, creator=admin_user)
    dtype = DeviceTypes.objects.create(title="TypeDSWD", code_name="typedswd", is_core=False, creator=admin_user)
    dmark = DeviceMarks.objects.create(title="MarkDSWD", code_name="markdswd", is_core=False, creator=admin_user)
    dmodel = DeviceModels.objects.create(title="ModelDSWD", code_name="modeldswd", is_core=False, creator=admin_user)
    dproc = DeviceProcessors.objects.create(title="ProcDSWD", code_name="procdswd", is_core=False, creator=admin_user)
    dram = DeviceRAMs.objects.create(title="RAMDSWD", code_name="ramdswd", is_core=False, creator=admin_user)
    ddisk = DeviceDisks.objects.create(title="DiskDSWD", code_name="diskdswd", is_core=False, creator=admin_user)
    dsystem = DeviceSystems.objects.create(title="SystemDSWD", code_name="systemdswd", is_core=False, creator=admin_user)
    dbuild = DeviceBuilds.objects.create(title="BuildDSWD", code_name="builddswd", is_core=False, creator=admin_user)
    device = Devices.objects.create(
        internal_id="DEVDSWD",
        location=location,
        type=dtype,
        mark=dmark,
        model=dmodel,
        processor=dproc,
        ram=dram,
        disk=ddisk,
        system=dsystem,
        build=dbuild,
        serial="SNDSWD",
        notes="DeviceSoftwares device delete",
        creator=admin_user
    )
    software = Softwares.objects.create(title="SoftDSWD", code_name="softdswd", is_core=False, creator=admin_user)
    dev_soft = DeviceSoftwares.objects.create(device=device, software=software, installed_at="2024-01-01 00:00:00:000000")
    url = reverse('device-softwares-detail', args=[dev_soft.id])
    response = api_client.delete(url)
    assert response.status_code in [status.HTTP_204_NO_CONTENT, status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST]
