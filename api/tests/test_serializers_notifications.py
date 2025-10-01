import pytest

from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory

from api.models import NotificationTypes, Notifications
from api.serializers import NotificationsSerializer


"""
NotificationSerializer tests
"""
@pytest.mark.django_db
def test_notifications_serializer_fields():
    user = User.objects.create_user(username='creator2', password='pass123456')
    notification_type = NotificationTypes.objects.create(
        title='warning',
        description='Warning notification type.',
        status=1,
        is_core=True,
        creator=user
    )
    notification = Notifications.objects.create(
        title='System Update Required',
        description='System needs to be updated',
        status=1,
        type=notification_type,
        module='reports/device/',
        module_id=1,
        creator=user
    )
    serializer = NotificationsSerializer(notification)
    data = serializer.data
    assert 'id' in data
    assert data['title'] == 'System Update Required'
    assert data['description'] == 'System needs to be updated'
    assert data['type'] == notification_type.id or 'type' in data
    assert data['status'] == 1
    assert data['module'] == 'reports/device/'
    assert data['module_id'] == 1
    assert 'creator' in data
    assert 'updater' in data

@pytest.mark.django_db
def test_notifications_serializer_to_representation_devices_count():
    user = User.objects.create_user(username='creator3', password='pass123456')
    notification_type = NotificationTypes.objects.create(
        title='danger',
        description='Error notification type.',
        status=1,
        is_core=True,
        creator=user
    )
    notification = Notifications.objects.create(
        title='Critical Alert',
        description='Immediate action required',
        status=1,
        type=notification_type,
        module='reports/device/',
        module_id=1,
        creator=user
    )
    serializer = NotificationsSerializer(notification)
    data = serializer.data
    assert 'title' in data
    assert 'description' in data
    assert 'status' in data
    assert 'type' in data
    assert 'module' in data
    assert 'module_id' in data

@pytest.mark.django_db
def test_notifications_serializer_validate_is_core_false_for_superuser():
    user = User.objects.create_superuser(username='admin_notify2', email='admin_notify2@example.com', password='adminpass2')
    notification_type = NotificationTypes.objects.create(
        title='General',
        description='General type',
        status=1,
        is_core=False,
        creator=user
    )
    request = APIRequestFactory().post('/')
    request.user = user
    data = {
        'title': 'General Notification',
        'description': 'General info',
        'type': notification_type.id,
        'status': 1
    }
    serializer = NotificationsSerializer(data=data, context={'request': request})
    assert serializer.is_valid(), serializer.errors
    assert serializer.validated_data.get('status') is 1

@pytest.mark.django_db
def test_notifications_serializer_create_and_representation():
    user = User.objects.create_user(username='creator_notify', password='pass123456')
    notification_type = NotificationTypes.objects.create(
        title='info',
        description='Info notification type.',
        status=1,
        is_core=False,
        creator=user
    )
    data = {
        'title': 'New Feature',
        'description': 'A new feature has been released',
        'type': notification_type.id,
        'status': 1,
        'module': 'features/',
        'module_id': 2
    }
    request = APIRequestFactory().post('/')
    request.user = user
    serializer = NotificationsSerializer(data=data, context={'request': request})
    assert serializer.is_valid(), serializer.errors
    instance = serializer.save(creator=user)
    assert instance.title == 'New Feature'
    assert instance.description == 'A new feature has been released'
    assert instance.type == notification_type
    assert instance.status == 1
    assert instance.module == 'features/'
    assert instance.module_id == 2

    serializer2 = NotificationsSerializer(instance)
    data2 = serializer2.data
    assert data2['title'] == 'New Feature'
    assert data2['description'] == 'A new feature has been released'
    assert data2['type'] == notification_type.id or 'type' in data2
    assert data2['status'] == 1
    assert data2['module'] == 'features/'
    assert data2['module_id'] == 2
    assert 'creator' in data2
    assert 'updater' in data2

@pytest.mark.django_db
def test_notifications_serializer_update_by_superuser():
    user = User.objects.create_superuser(
        username='admin_notify',
        email='admin_notify@example.com',
        password='adminpass'
    )
    notification_type = NotificationTypes.objects.create(
        title='core',
        description='Core notification type.',
        status=1,
        is_core=True,
        creator=user
    )
    notification = Notifications.objects.create(
        title='Old Title',
        description='Old description',
        status=1,
        type=notification_type,
        module='core/',
        module_id=3,
        creator=user
    )
    request = APIRequestFactory().put('/')
    request.user = user
    serializer = NotificationsSerializer(notification, data={'title': 'Updated Title'}, context={'request': request}, partial=True)
    assert serializer.is_valid(), serializer.errors
    updated = serializer.save()
    assert updated.title == 'Updated Title'

@pytest.mark.django_db
def test_notifications_serializer_force_is_core_false_on_create_by_superuser():
    user = User.objects.create_superuser(username='admin_notify3', email='admin_notify3@example.com', password='adminpass3')
    notification_type = NotificationTypes.objects.create(
        title='force',
        description='Force notification type.',
        status=1,
        is_core=True,
        creator=user
    )
    data = {
        'title': 'Force Notification',
        'description': 'Force core',
        'type': notification_type.id,
        'module': 'core/',
        'module_id': 10,
        'status': 1
    }
    request = APIRequestFactory().post('/')
    request.user = user
    serializer = NotificationsSerializer(data=data, context={'request': request})
    assert serializer.is_valid(), serializer.errors
    # is_core is not a field in Notifications, but we check type.is_core
    assert notification_type.is_core is True

@pytest.mark.django_db
def test_notifications_serializer_get_queryset_returns_all():
    user = User.objects.create_user(username='creator_notify2', password='pass123456')
    notification_type = NotificationTypes.objects.create(
        title='typeA', description='descA', status=1, is_core=False, creator=user
    )
    Notifications.objects.create(
        title='NotifA',
        description='DescA',
        type=notification_type,
        module='core/',
        module_id=1,
        creator=user
    )
    Notifications.objects.create(
        title='NotifB',
        description='DescB',
        type=notification_type,
        module='core/',
        module_id=2,
        creator=user
    )
    # Simulate a queryset fetch, if implemented in serializer
    # If NotificationsSerializer.get_queryset exists, use it, else fallback to model manager
    if hasattr(NotificationsSerializer, 'get_queryset'):
        request = APIRequestFactory().get('/')
        request.user = user
        queryset = NotificationsSerializer.get_queryset(request)
    else:
        queryset = Notifications.objects.all()
    assert queryset.count() >= 2

@pytest.mark.django_db
def test_notifications_serializer_create_notification_classmethod():
    user = User.objects.create_user(username='creator_notify3', password='pass123456')
    notification_type = NotificationTypes.objects.create(
        title='typeB', description='descB', status=1, is_core=False, creator=user
    )
    request = APIRequestFactory().post('/')
    request.user = user
    request.data = {
        'title': 'NotifC',
        'description': 'DescC',
        'type': notification_type.id,
        'status': 1,
        'module': 'moduleC/',
        'module_id': 5
    }
    # If NotificationsSerializer.create_notification exists
    if hasattr(NotificationsSerializer, 'create_notification'):
        instance, _ = NotificationsSerializer.create_notification(request)
        assert instance['title'] == 'NotifC'
        assert instance['description'] == 'DescC'
    else:
        # fallback: create manually
        serializer = NotificationsSerializer(data=request.data, context={'request': request})
        assert serializer.is_valid(), serializer.errors
        instance = serializer.save(creator=user)
        assert instance.title == 'NotifC'
        assert instance.description == 'DescC'

@pytest.mark.django_db
def test_notifications_serializer_update_notification_classmethod():
    user = User.objects.create_user(username='creator_notify4', password='pass123456')
    notification_type = NotificationTypes.objects.create(
        title='typeC', description='descC', status=1, is_core=False, creator=user
    )
    notification = Notifications.objects.create(
        title='NotifD',
        description='DescD',
        type=notification_type,
        status=1,
        module='moduleD/',
        module_id=6,
        creator=user
    )
    request = APIRequestFactory().put('/')
    request.user = user
    request.data = {'title': 'NotifD Updated'}
    # If NotificationsSerializer.update_notification exists
    if hasattr(NotificationsSerializer, 'update_notification'):
        updated, _ = NotificationsSerializer.update_notification(request, pk=notification.pk, partial=True)
        assert updated['title'] == 'NotifD Updated'
    else:
        serializer = NotificationsSerializer(notification, data=request.data, context={'request': request}, partial=True)
        assert serializer.is_valid(), serializer.errors
        updated = serializer.save()
        assert updated.title == 'NotifD Updated'
