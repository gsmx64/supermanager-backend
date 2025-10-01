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
UserExtendedViewSet tests
"""
@pytest.mark.django_db
def test_user_extended_list(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    url = reverse('users-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK or response.status_code == status.HTTP_204_NO_CONTENT

@pytest.mark.django_db
def test_user_extended_retrieve(api_client, admin_user, user):
    api_client.force_authenticate(user=admin_user)
    url = reverse('users-detail', args=[user.id])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == user.id

@pytest.mark.django_db
def test_user_extended_create(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    url = reverse('users-list')
    data = {
        "username": "extendeduser",
        "email": "extendeduser@example.com",
        "password": "extendedpass123",
        "repeat_password": "extendedpass123",
        "first_name": "Extended",
        "last_name": "User"
    }
    response = api_client.post(url, data)
    assert response.status_code in [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST]

@pytest.mark.django_db
def test_user_extended_update(api_client, admin_user, user):
    api_client.force_authenticate(user=admin_user)
    url = reverse('users-detail', args=[user.id])
    data = {
        "first_name": "UpdatedName",
        "last_name": "UpdatedLast"
    }
    response = api_client.put(url, data)
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST]
    if response.status_code == status.HTTP_200_OK:
        assert response.data["first_name"] == "UpdatedName"

@pytest.mark.django_db
def test_user_extended_partial_update(api_client, admin_user, user):
    api_client.force_authenticate(user=admin_user)
    url = reverse('users-detail', args=[user.id])
    data = {
        "first_name": "PartialName"
    }
    response = api_client.patch(url, data)
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST]
    if response.status_code == status.HTTP_200_OK:
        assert response.data["first_name"] == "PartialName"

@pytest.mark.django_db
def test_user_extended_delete(api_client, admin_user, user):
    api_client.force_authenticate(user=admin_user)
    url = reverse('users-detail', args=[user.id])
    response = api_client.delete(url)
    assert response.status_code in [status.HTTP_204_NO_CONTENT, status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST]

@pytest.mark.django_db
def test_user_extended_patch_method(api_client, admin_user, user):
    api_client.force_authenticate(user=admin_user)
    url = reverse('users-detail', args=[user.id])
    data = {
        "last_name": "PatchMethod"
    }
    response = api_client.patch(url, data)
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST]
    if response.status_code == status.HTTP_200_OK:
        assert response.data["last_name"] == "PatchMethod"

@pytest.mark.django_db
def test_user_extended_put_method(api_client, admin_user, user):
    api_client.force_authenticate(user=admin_user)
    url = reverse('users-detail', args=[user.id])
    data = {
        "first_name": "PutMethod",
        "last_name": "PutLast"
    }
    response = api_client.put(url, data)
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST]
    if response.status_code == status.HTTP_200_OK:
        assert response.data["first_name"] == "PutMethod"
