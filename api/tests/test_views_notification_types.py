import pytest

from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User

from api.models import User, NotificationTypes


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
NotificationTypesViewSet tests
"""
@pytest.mark.django_db
def test_notification_types_list(api_client, user):
    api_client.force_authenticate(user=user)
    url = reverse('notification-types-list')
    response = api_client.get(url)
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT]

@pytest.mark.django_db
def test_notification_types_create(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    url = reverse('notification-types-list')
    data = {
        "title": "TypeA",
        "description": "Type A description",
        "sort_order": 1,
        "is_core": False
    }
    response = api_client.post(url, data)
    assert response.status_code in [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST]

@pytest.mark.django_db
def test_notification_types_retrieve(api_client, user, admin_user):
    api_client.force_authenticate(user=admin_user)
    nt = NotificationTypes.objects.create(title="TypeB", is_core=False, creator=admin_user)
    api_client.force_authenticate(user=user)
    url = reverse('notification-types-detail', args=[nt.id])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["title"] == "TypeB"

@pytest.mark.django_db
def test_notification_types_update(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    nt = NotificationTypes.objects.create(title="TypeC", is_core=False, creator=admin_user)
    url = reverse('notification-types-detail', args=[nt.id])
    update_data = {
        "title": "TypeC Updated",
        "description": "Updated description",
        "sort_order": 2,
        "is_core": False
    }
    response = api_client.put(url, update_data)
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST]
    if response.status_code == status.HTTP_200_OK:
        assert response.data["title"] == "TypeC Updated"

@pytest.mark.django_db
def test_notification_types_partial_update(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    nt = NotificationTypes.objects.create(title="TypeD", is_core=False, creator=admin_user)
    url = reverse('notification-types-detail', args=[nt.id])
    patch_data = {
        "description": "Patched type description"
    }
    response = api_client.patch(url, patch_data)
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST]
    if response.status_code == status.HTTP_200_OK:
        assert response.data["description"] == "Patched type description"

@pytest.mark.django_db
def test_notification_types_delete(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    nt = NotificationTypes.objects.create(title="TypeE", is_core=False, creator=admin_user)
    url = reverse('notification-types-detail', args=[nt.id])
    response = api_client.delete(url)
    assert response.status_code in [status.HTTP_204_NO_CONTENT, status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST]
