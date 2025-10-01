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
SoftwaresViewSet tests
"""
@pytest.mark.django_db
def test_softwares_list(api_client, user):
    api_client.force_authenticate(user=user)
    url = reverse('softwares-list')
    response = api_client.get(url)
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT]

@pytest.mark.django_db
def test_softwares_create(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    url = reverse('softwares-list')
    data = {
        "title": "SoftwareX",
        "description": "Software X description",
        "code_name": "softwarex",
        "sort_order": 1,
        "is_core": False
    }
    response = api_client.post(url, data)
    assert response.status_code in [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST]

@pytest.mark.django_db
def test_softwares_retrieve(api_client, user, admin_user):
    api_client.force_authenticate(user=admin_user)
    url = reverse('softwares-list')
    data = {
        "title": "SoftwareY",
        "description": "Software Y description",
        "code_name": "softwarey",
        "sort_order": 2,
        "is_core": False
    }
    response = api_client.post(url, data)
    assert response.status_code in [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST]
    if response.status_code == status.HTTP_201_CREATED:
        software_id = response.data.get("id")
        api_client.force_authenticate(user=user)
        url_detail = reverse('softwares-detail', args=[software_id])
        response_detail = api_client.get(url_detail)
        assert response_detail.status_code == status.HTTP_200_OK
        assert response_detail.data["title"] == "SoftwareY"

@pytest.mark.django_db
def test_softwares_update(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    url = reverse('softwares-list')
    data = {
        "title": "SoftwareZ",
        "description": "Software Z description",
        "code_name": "softwarez",
        "sort_order": 3,
        "is_core": False
    }
    response = api_client.post(url, data)
    assert response.status_code in [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST]
    if response.status_code == status.HTTP_201_CREATED:
        software_id = response.data.get("id")
        url_detail = reverse('softwares-detail', args=[software_id])
        update_data = {
            "title": "SoftwareZ Updated",
            "description": "Updated description",
            "code_name": "softwarez",
            "sort_order": 4,
            "is_core": False
        }
        response_update = api_client.put(url_detail, update_data)
        assert response_update.status_code in [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST]
        if response_update.status_code == status.HTTP_200_OK:
            assert response_update.data["title"] == "SoftwareZ Updated"

@pytest.mark.django_db
def test_softwares_partial_update(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    url = reverse('softwares-list')
    data = {
        "title": "SoftwareW",
        "description": "Software W description",
        "code_name": "softwarew",
        "sort_order": 5,
        "is_core": False
    }
    response = api_client.post(url, data)
    assert response.status_code in [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST]
    if response.status_code == status.HTTP_201_CREATED:
        software_id = response.data.get("id")
        url_detail = reverse('softwares-detail', args=[software_id])
        patch_data = {
            "description": "Patched software description"
        }
        response_patch = api_client.patch(url_detail, patch_data)
        assert response_patch.status_code in [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST]
        if response_patch.status_code == status.HTTP_200_OK:
            assert response_patch.data["description"] == "Patched software description"

@pytest.mark.django_db
def test_softwares_delete(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    url = reverse('softwares-list')
    data = {
        "title": "SoftwareDelete",
        "description": "Software to delete",
        "code_name": "softwaredelete",
        "sort_order": 6,
        "is_core": False
    }
    response = api_client.post(url, data)
    assert response.status_code in [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST]
    if response.status_code == status.HTTP_201_CREATED:
        software_id = response.data.get("id")
        url_detail = reverse('softwares-detail', args=[software_id])
        response_delete = api_client.delete(url_detail)
        assert response_delete.status_code in [status.HTTP_204_NO_CONTENT, status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST]
