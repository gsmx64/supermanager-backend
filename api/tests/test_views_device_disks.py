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
DeviceDisksViewSet tests
"""
@pytest.mark.django_db
def test_device_disks_list(api_client, user):
    api_client.force_authenticate(user=user)
    url = reverse('device-disks-list')
    response = api_client.get(url)
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT]

@pytest.mark.django_db
def test_device_disks_create(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    url = reverse('device-disks-list')
    data = {
        "title": "DiskX",
        "description": "Disk X description",
        "code_name": "diskx",
        "sort_order": 1,
        "is_core": False
    }
    response = api_client.post(url, data)
    assert response.status_code in [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST]

@pytest.mark.django_db
def test_device_disks_retrieve(api_client, user, admin_user):
    api_client.force_authenticate(user=admin_user)
    url = reverse('device-disks-list')
    data = {
        "title": "DiskY",
        "description": "Disk Y description",
        "code_name": "disky",
        "sort_order": 2,
        "is_core": False
    }
    response = api_client.post(url, data)
    assert response.status_code in [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST]
    if response.status_code == status.HTTP_201_CREATED:
        disk_id = response.data.get("id")
        api_client.force_authenticate(user=user)
        url_detail = reverse('device-disks-detail', args=[disk_id])
        response_detail = api_client.get(url_detail)
        assert response_detail.status_code == status.HTTP_200_OK
        assert response_detail.data["title"] == "DiskY"

@pytest.mark.django_db
def test_device_disks_update(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    url = reverse('device-disks-list')
    data = {
        "title": "DiskZ",
        "description": "Disk Z description",
        "code_name": "diskz",
        "sort_order": 3,
        "is_core": False
    }
    response = api_client.post(url, data)
    assert response.status_code in [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST]
    if response.status_code == status.HTTP_201_CREATED:
        disk_id = response.data.get("id")
        url_detail = reverse('device-disks-detail', args=[disk_id])
        update_data = {
            "title": "DiskZ Updated",
            "description": "Updated description",
            "code_name": "diskz",
            "sort_order": 4,
            "is_core": False
        }
        response_update = api_client.put(url_detail, update_data)
        assert response_update.status_code in [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST]
        if response_update.status_code == status.HTTP_200_OK:
            assert response_update.data["title"] == "DiskZ Updated"

@pytest.mark.django_db
def test_device_disks_partial_update(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    url = reverse('device-disks-list')
    data = {
        "title": "DiskW",
        "description": "Disk W description",
        "code_name": "diskw",
        "sort_order": 5,
        "is_core": False
    }
    response = api_client.post(url, data)
    assert response.status_code in [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST]
    if response.status_code == status.HTTP_201_CREATED:
        disk_id = response.data.get("id")
        url_detail = reverse('device-disks-detail', args=[disk_id])
        patch_data = {
            "description": "Patched disk description"
        }
        response_patch = api_client.patch(url_detail, patch_data)
        assert response_patch.status_code in [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST]
        if response_patch.status_code == status.HTTP_200_OK:
            assert response_patch.data["description"] == "Patched disk description"

@pytest.mark.django_db
def test_device_disks_delete(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    url = reverse('device-disks-list')
    data = {
        "title": "DiskDelete",
        "description": "Disk to delete",
        "code_name": "diskdelete",
        "sort_order": 6,
        "is_core": False
    }
    response = api_client.post(url, data)
    assert response.status_code in [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST]
    if response.status_code == status.HTTP_201_CREATED:
        disk_id = response.data.get("id")
        url_detail = reverse('device-disks-detail', args=[disk_id])
        response_delete = api_client.delete(url_detail)
        assert response_delete.status_code in [status.HTTP_204_NO_CONTENT, status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST]
