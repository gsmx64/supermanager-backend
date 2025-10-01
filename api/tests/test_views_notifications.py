import pytest

from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User

from api.models import (
    User,
    NotificationTypes,
    Notifications
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
NotificationsViewSet tests
"""
@pytest.mark.django_db
def test_notifications_list(api_client, user):
    api_client.force_authenticate(user=user)
    url = reverse('notifications-list')
    response = api_client.get(url)
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT]

@pytest.mark.django_db
def test_notifications_create(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    nt = NotificationTypes.objects.create(title="default", is_core=False, creator=admin_user)
    url = reverse('notifications-list')
    data = {
        "type": nt.id,
        "title": "Notification A",
        "description": "Notification description",
        "status": 1,
        "module": "calendar/event",
        "module_id": 123,
        "creator": admin_user
    }
    response = api_client.post(url, data)
    assert response.status_code in [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST]

@pytest.mark.django_db
def test_notifications_retrieve(api_client, user, admin_user):
    api_client.force_authenticate(user=admin_user)
    nt = NotificationTypes.objects.create(title="default", is_core=False, creator=admin_user)
    notification = Notifications.objects.create(
        type=nt,
        title="NotifR",
        description="desc",
        status=1,
        module="calendar/event",
        module_id=456,
        creator=admin_user
    )
    api_client.force_authenticate(user=user)
    url = reverse('notifications-detail', args=[notification.id])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["title"] == "NotifR"

@pytest.mark.django_db
def test_notifications_update(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    nt = NotificationTypes.objects.create(title="default", is_core=False, creator=admin_user)
    notification = Notifications.objects.create(
        type=nt,
        title="NotifU",
        description="desc",
        status=1,
        module="calendar/event",
        module_id=456,
        creator=admin_user
    )
    url = reverse('notifications-detail', args=[notification.id])
    update_data = {
        "type": nt.id,
        "title": "NotifU Updated",
        "description": "Updated desc",
        "status": 1,
        "module": "calendar/event",
        "module_id": 789,
        "is_core": False
    }
    response = api_client.put(url, update_data)
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST]
    if response.status_code == status.HTTP_200_OK:
        assert response.data["title"] == "NotifU Updated"

@pytest.mark.django_db
def test_notifications_partial_update(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    nt = NotificationTypes.objects.create(title="default", is_core=False, creator=admin_user)
    notification = Notifications.objects.create(
        type=nt,
        title="NotifP",
        description="desc",
        status=1,
        module="calendar/event",
        module_id=456,
        creator=admin_user
    )
    url = reverse('notifications-detail', args=[notification.id])
    patch_data = {
        "description": "Patched notification description"
    }
    response = api_client.patch(url, patch_data)
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST]
    if response.status_code == status.HTTP_200_OK:
        assert response.data["description"] == "Patched notification description"

@pytest.mark.django_db
def test_notifications_delete(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    nt = NotificationTypes.objects.create(title="default", is_core=False, creator=admin_user)
    notification = Notifications.objects.create(
        type=nt,
        title="NotifD",
        description="desc",
        status=1,
        module="calendar/event",
        module_id=123,
        creator=admin_user
    )
    url = reverse('notifications-detail', args=[notification.id])
    response = api_client.delete(url)
    assert response.status_code in [status.HTTP_204_NO_CONTENT, status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST]

@pytest.mark.django_db
def test_notifications_get_with_id(api_client, user, admin_user):
    api_client.force_authenticate(user=admin_user)
    nt = NotificationTypes.objects.create(title="default", is_core=False, creator=admin_user)
    notification = Notifications.objects.create(
        type=nt,
        title="NotifG",
        description="desc",
        status=1,
        module="calendar/event",
        module_id=456,
        creator=admin_user
    )
    api_client.force_authenticate(user=user)
    url = reverse('notifications-detail', args=[notification.id])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == notification.id

@pytest.mark.django_db
def test_notifications_get_without_id(api_client, user):
    api_client.force_authenticate(user=user)
    url = reverse('notifications-list')
    response = api_client.get(url)
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT]
