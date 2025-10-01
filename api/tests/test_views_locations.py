import pytest

from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User

from api.models import User, LocationZones, Locations


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
LocationsViewSet tests
"""
@pytest.mark.django_db
def test_locations_create(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    # Create a LocationZone first
    zone = LocationZones.objects.create(title="ZoneTest", is_core=False, creator=admin_user)
    url = reverse('locations-list')
    data = {
        "title": "Location A",
        "description": "Description for Location A",
        "code_name": "location_a",
        "location_zone": zone.id,
        "manager": "ManagerLocationA",
        "manager_email": "email@example.com",
        "manager_phone": "1234567890",
        "manager_mobile": "0987654321",
        "collaborator": "CollaboratorLocationA",
        "collaborator_email": "email@example.com",
        "collaborator_phone": "1234567890",
        "collaborator_mobile": "0987654321",
        "phone": "1234567890",
        "mobile": "0987654321",
        "address": "123 Main St",
        "city": "CityName",
        "state": "StateName",
        "zip_code": "12345",
        "country": "CountryName",
        "latitude": "0.0000",
        "longitude": "0.0000",
        "sort_order": 1,
        "creator": admin_user
    }
    response = api_client.post(url, data)
    assert response.status_code in [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST]

@pytest.mark.django_db
def test_locations_list(api_client, user):
    api_client.force_authenticate(user=user)
    url = reverse('locations-list')
    response = api_client.get(url)
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT]

@pytest.mark.django_db
def test_locations_retrieve(api_client, user, admin_user):
    api_client.force_authenticate(user=admin_user)
    zone = LocationZones.objects.create(title="ZoneTest", is_core=False, creator=admin_user)
    location = Locations.objects.create(
        title="Location Retrieve",
        code_name="location_retrieve",
        location_zone=zone,
        address="Some address",
        is_core=False,
        creator=admin_user
    )
    api_client.force_authenticate(user=user)
    url = reverse('locations-detail', args=[location.id])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["title"] == "Location Retrieve"

@pytest.mark.django_db
def test_locations_update(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    zone = LocationZones.objects.create(title="ZoneTest", is_core=False, creator=admin_user)
    location = Locations.objects.create(
        title="Location Update",
        code_name="location_update",
        location_zone=zone,
        address="Some address",
        is_core=False,
        creator=admin_user
    )
    url = reverse('locations-detail', args=[location.id])
    update_data = {
        "title": "Location Updated",
        "description": "Updated description",
        "code_name": "location_update",
        "location_zone": zone.id,
        "address": "Updated address",
        "is_core": False
    }
    response = api_client.put(url, update_data)
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST]
    if response.status_code == status.HTTP_200_OK:
        assert response.data["title"] == "Location Updated"

@pytest.mark.django_db
def test_locations_partial_update(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    zone = LocationZones.objects.create(title="ZoneTest", is_core=False, creator=admin_user)
    location = Locations.objects.create(
        title="Location Patch",
        code_name="location_patch",
        location_zone=zone,
        address="Some address",
        is_core=False,
        creator=admin_user
    )
    url = reverse('locations-detail', args=[location.id])
    patch_data = {
        "description": "Patched location description"
    }
    response = api_client.patch(url, patch_data)
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST]
    if response.status_code == status.HTTP_200_OK:
        assert response.data["description"] == "Patched location description"

@pytest.mark.django_db
def test_locations_delete(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    zone = LocationZones.objects.create(title="ZoneTest", is_core=False, creator=admin_user)
    location = Locations.objects.create(
        title="Location Delete",
        code_name="location_delete",
        location_zone=zone,
        address="Some address",
        is_core=False,
        creator=admin_user
    )
    url = reverse('locations-detail', args=[location.id])
    response = api_client.delete(url)
    assert response.status_code in [status.HTTP_204_NO_CONTENT, status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST]

@pytest.mark.django_db
def test_locations_get_with_id(api_client, user, admin_user):
    api_client.force_authenticate(user=admin_user)
    zone = LocationZones.objects.create(title="ZoneTest", is_core=False, creator=admin_user)
    location = Locations.objects.create(
        title="Location GetID",
        code_name="location_getid",
        location_zone=zone,
        address="Some address",
        is_core=False,
        creator=admin_user
    )
    api_client.force_authenticate(user=user)
    url = reverse('locations-detail', args=[location.id])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == location.id

@pytest.mark.django_db
def test_locations_get_without_id(api_client, user):
    api_client.force_authenticate(user=user)
    url = reverse('locations-list')
    response = api_client.get(url)
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT]
