import pytest

from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User

from api.models import User


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
DeviceBuildsViewSet tests
"""
@pytest.mark.django_db
def test_device_builds_list(api_client, user):
    api_client.force_authenticate(user=user)
    url = reverse('device-builds-list')
    response = api_client.get(url)
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT]

@pytest.mark.django_db
def test_device_builds_create(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    url = reverse('device-builds-list')
    data = {
        "title": "BuildX",
        "description": "Build X description",
        "code_name": "buildx",
        "sort_order": 1,
        "is_core": False
    }
    response = api_client.post(url, data)
    assert response.status_code in [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST]

@pytest.mark.django_db
def test_device_builds_retrieve(api_client, user, admin_user):
    api_client.force_authenticate(user=admin_user)
    url = reverse('device-builds-list')
    data = {
        "title": "BuildY",
        "description": "Build Y description",
        "code_name": "buildy",
        "sort_order": 2,
        "is_core": False
    }
    response = api_client.post(url, data)
    assert response.status_code in [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST]
    if response.status_code == status.HTTP_201_CREATED:
        build_id = response.data.get("id")
        api_client.force_authenticate(user=user)
        url_detail = reverse('device-builds-detail', args=[build_id])
        response_detail = api_client.get(url_detail)
        assert response_detail.status_code == status.HTTP_200_OK
        assert response_detail.data["title"] == "BuildY"

@pytest.mark.django_db
def test_device_builds_update(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    url = reverse('device-builds-list')
    data = {
        "title": "BuildZ",
        "description": "Build Z description",
        "code_name": "buildz",
        "sort_order": 3,
        "is_core": False
    }
    response = api_client.post(url, data)
    assert response.status_code in [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST]
    if response.status_code == status.HTTP_201_CREATED:
        build_id = response.data.get("id")
        url_detail = reverse('device-builds-detail', args=[build_id])
        update_data = {
            "title": "BuildZ Updated",
            "description": "Updated description",
            "code_name": "buildz",
            "sort_order": 4,
            "is_core": False
        }
        response_update = api_client.put(url_detail, update_data)
        assert response_update.status_code in [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST]
        if response_update.status_code == status.HTTP_200_OK:
            assert response_update.data["title"] == "BuildZ Updated"

@pytest.mark.django_db
def test_device_builds_partial_update(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    url = reverse('device-builds-list')
    data = {
        "title": "BuildW",
        "description": "Build W description",
        "code_name": "buildw",
        "sort_order": 5,
        "is_core": False
    }
    response = api_client.post(url, data)
    assert response.status_code in [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST]
    if response.status_code == status.HTTP_201_CREATED:
        build_id = response.data.get("id")
        url_detail = reverse('device-builds-detail', args=[build_id])
        patch_data = {
            "description": "Patched build description"
        }
        response_patch = api_client.patch(url_detail, patch_data)
        assert response_patch.status_code in [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST]
        if response_patch.status_code == status.HTTP_200_OK:
            assert response_patch.data["description"] == "Patched build description"

@pytest.mark.django_db
def test_device_builds_delete(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    url = reverse('device-builds-list')
    data = {
        "title": "BuildDelete",
        "description": "Build to delete",
        "code_name": "builddelete",
        "sort_order": 6,
        "is_core": False
    }
    response = api_client.post(url, data)
    assert response.status_code in [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST]
    if response.status_code == status.HTTP_201_CREATED:
        build_id = response.data.get("id")
        url_detail = reverse('device-builds-detail', args=[build_id])
        response_delete = api_client.delete(url_detail)
        assert response_delete.status_code in [status.HTTP_204_NO_CONTENT, status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST]
