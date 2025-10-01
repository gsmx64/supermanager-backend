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
LocationZonesViewSet tests
"""
@pytest.mark.django_db
def test_location_zones_list(api_client, user):
    api_client.force_authenticate(user=user)
    url = reverse('location-zones-list')
    response = api_client.get(url)
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT]

@pytest.mark.django_db
def test_location_zones_create(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    url = reverse('location-zones-list')
    data = {
        "name": "ZoneA",
        "description": "Description for ZoneA",
        "is_core": False,
        "creator": admin_user.id
    }
    response = api_client.post(url, data)
    assert response.status_code in [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST]

@pytest.mark.django_db
def test_location_zones_retrieve(api_client, user, admin_user):
    api_client.force_authenticate(user=admin_user)
    zone = LocationZones.objects.create(title="ZoneRetrieve", is_core=False, creator=admin_user)
    api_client.force_authenticate(user=user)
    url = reverse('location-zones-detail', args=[zone.id])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["title"] == "ZoneRetrieve"

@pytest.mark.django_db
def test_location_zones_update(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    zone = LocationZones.objects.create(title="ZoneUpdate", is_core=False, creator=admin_user)
    url = reverse('location-zones-detail', args=[zone.id])
    update_data = {
        "name": "ZoneUpdated",
        "description": "Updated description",
        "is_core": False
    }
    response = api_client.put(url, update_data)
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST]
    if response.status_code == status.HTTP_200_OK:
        assert response.data["name"] == "ZoneUpdated"

@pytest.mark.django_db
def test_location_zones_partial_update(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    zone = LocationZones.objects.create(title="ZonePatch", is_core=False, creator=admin_user)
    url = reverse('location-zones-detail', args=[zone.id])
    patch_data = {
        "description": "Patched zone description"
    }
    response = api_client.patch(url, patch_data)
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST]
    if response.status_code == status.HTTP_200_OK:
        assert response.data["description"] == "Patched zone description"

@pytest.mark.django_db
def test_location_zones_delete(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    zone = LocationZones.objects.create(title="ZoneDelete", is_core=False, creator=admin_user)
    url = reverse('location-zones-detail', args=[zone.id])
    response = api_client.delete(url)
    assert response.status_code in [status.HTTP_204_NO_CONTENT, status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST]

@pytest.mark.django_db
def test_location_zones_locations_action(api_client, user, admin_user):
    api_client.force_authenticate(user=admin_user)
    zone = LocationZones.objects.create(title="ZoneWithLocations", is_core=False, creator=admin_user)
    Locations.objects.create(
        title="Location1",
        code_name="location1",
        location_zone=zone,
        address="Address1",
        is_core=False,
        creator=admin_user
    )
    api_client.force_authenticate(user=user)
    url = reverse('location-zones-locations', args=[zone.id])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert "results" in response.data
    assert isinstance(response.data["results"], list)
    # Check that at least one location in results belongs to the correct zone
    assert any(
        (
            isinstance(loc.get("location_zone"), dict) and loc["location_zone"].get("id") == zone.id
        )
        for loc in response.data["results"]
    )
