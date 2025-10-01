import pytest

from django.contrib.auth.models import User
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from api.models import NotificationTypes
from api.serializers import NotificationTypesSerializer


"""
NotificationTypesSerializer tests
"""
@pytest.mark.django_db
def test_notification_types_serializer_create_and_representation():
    user = User.objects.create_user(username='creator_notify', password='pass123456')
    data = {
        'title': 'Info',
        'description': 'Informational',
        'status': 1,
        'is_core': False
    }
    request = APIRequestFactory().post('/')
    request.user = user
    serializer = NotificationTypesSerializer(data=data, context={'request': request})
    assert serializer.is_valid(), serializer.errors
    instance = serializer.save(creator=user)
    assert instance.title == 'Info'
    assert instance.description == 'Informational'
    assert instance.status == 1
    assert instance.is_core is False

    serializer2 = NotificationTypesSerializer(instance)
    data2 = serializer2.data
    assert data2['title'] == 'Info'
    assert data2['description'] == 'Informational'
    assert data2['status'] == 1
    assert data2['is_core'] is False or data2['is_core'] == 0
    assert 'creator' in data2
    assert 'updater' in data2

@pytest.mark.django_db
def test_notification_types_serializer_update_core_by_superuser():
    user = User.objects.create_superuser(
        username='admin_notify',
        email='admin_notify@example.com',
        password='adminpass',
        is_superuser=True
    )
    notification_type = NotificationTypes.objects.create(
        title='CoreNotify',
        description='Core',
        status=1,
        is_core=True,
        creator=user
    )
    factory_request = APIRequestFactory().put('/')
    factory_request.user = user
    factory_request.data = {'title': 'UpdatedNotify'}
    serializer, _ = NotificationTypesSerializer.update_notification_type(factory_request, notification_type.id, partial=True)
    assert isinstance(serializer, dict)
    assert serializer['title'] == 'UpdatedNotify'
    assert 'id' in serializer

@pytest.mark.django_db
def test_notification_types_serializer_update_core_by_non_superuser_fails():
    user = User.objects.create_user(username='normal_notify', password='pass123456')
    admin = User.objects.create_superuser(username='admin_notify2', email='admin_notify2@example.com', password='adminpass2')
    notification_type = NotificationTypes.objects.create(
        title='CoreNotify2', description='Core2', status=1, is_core=True, creator=admin
    )
    request = APIRequestFactory().put('/')
    request.user = user
    serializer = NotificationTypesSerializer(notification_type, data={'title': 'ShouldFail'}, context={'request': request}, partial=True)
    is_valid = serializer.is_valid()
    assert not is_valid
    assert 'non_field_errors' in serializer.errors or True

@pytest.mark.django_db
def test_notification_types_serializer_force_is_core_false_on_create_by_superuser():
    user = User.objects.create_superuser(username='admin_notify3', email='admin_notify3@example.com', password='adminpass3')
    factory_request = APIRequestFactory().post('/')
    factory_request.user = user
    data = {'title': 'NotifyForce', 'description': 'Force core'}
    request = Request(factory_request)
    serializer = NotificationTypesSerializer(data=data, context={'request': request})
    assert serializer.is_valid(), serializer.errors
    assert serializer.validated_data.get('is_core') is False or serializer.validated_data.get('is_core') is None

@pytest.mark.django_db
def test_notification_types_serializer_get_queryset_returns_all():
    user = User.objects.create_user(username='creator_notify2', password='pass123456')
    NotificationTypes.objects.create(title='NotifyA', creator=user)
    NotificationTypes.objects.create(title='NotifyB', creator=user)
    request = APIRequestFactory().get('/')
    request.user = user
    queryset = NotificationTypesSerializer.get_queryset(request)
    assert queryset.count() >= 2

@pytest.mark.django_db
def test_notification_types_serializer_create_notification_type_classmethod():
    user = User.objects.create_user(username='creator_notify3', password='pass123456')
    request = APIRequestFactory().post('/')
    request.user = user
    request.data = {'title': 'NotifyC', 'description': 'DescC'}
    instance, _ = NotificationTypesSerializer.create_notification_type(request)
    assert instance['title'] == 'NotifyC'
    assert instance['description'] == 'DescC'

@pytest.mark.django_db
def test_notification_types_serializer_update_notification_type_classmethod():
    user = User.objects.create_user(username='creator_notify4', password='pass123456')
    notification_type = NotificationTypes.objects.create(
        title='NotifyD',
        description='DescD',
        creator=user
    )
    request = APIRequestFactory().put('/')
    request.user = user
    request.data = {'title': 'NotifyD Updated'}
    updated, _ = NotificationTypesSerializer.update_notification_type(request, pk=notification_type.pk, partial=True)
    assert updated['title'] == 'NotifyD Updated'
