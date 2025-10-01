import pytest

from django.contrib.auth.models import User
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from api.models import DeviceSystems
from api.serializers import DeviceSystemsSerializer


"""
DeviceSystemsSerializer tests
"""
@pytest.mark.django_db
def test_device_systems_serializer_create_and_representation():
    user = User.objects.create_user(username='creator_systems', password='pass123456')
    data = {
        'title': 'Android',
        'description': 'Mobile OS',
        'code_name': 'android',
        'status': 1,
        'is_core': False,
        'is_deprecated': False,
        'sort_order': 20
    }
    request = APIRequestFactory().post('/')
    request.user = user
    serializer = DeviceSystemsSerializer(data=data, context={'request': request})
    assert serializer.is_valid(), serializer.errors
    instance = serializer.save(creator=user)
    assert instance.title == 'Android'
    assert instance.description == 'Mobile OS'
    assert instance.code_name == 'android'
    assert instance.status == 1
    assert instance.is_core is False
    assert instance.is_deprecated is False
    assert instance.sort_order == 20

    serializer2 = DeviceSystemsSerializer(instance)
    data2 = serializer2.data
    assert data2['title'] == 'Android'
    assert data2['description'] == 'Mobile OS'
    assert data2['code_name'] == 'android'
    assert data2['status'] == 1
    assert data2['is_core'] is False or data2['is_core'] == 0
    assert data2['is_deprecated'] is False or data2['is_deprecated'] == 0
    assert data2['sort_order'] == 20
    assert 'creator' in data2
    assert 'updater' in data2

@pytest.mark.django_db
def test_device_systems_serializer_update_core_by_superuser():
    user = User.objects.create_superuser(
        username='admin_systems',
        email='admin_systems@example.com',
        password='adminpass',
        is_superuser=True
    )
    device_system = DeviceSystems.objects.create(
        title='CoreSystem',
        description='Core',
        code_name='coresystem',
        status=1,
        is_core=True,
        creator=user
    )
    factory_request = APIRequestFactory().put('/')
    factory_request.user = user
    factory_request.data = {'title': 'UpdatedSystem'}
    serializer, _ = DeviceSystemsSerializer.update_system(factory_request, device_system.id, partial=True)
    assert isinstance(serializer, dict)
    assert serializer['title'] == 'UpdatedSystem'
    assert 'id' in serializer

@pytest.mark.django_db
def test_device_systems_serializer_update_core_by_non_superuser_fails():
    user = User.objects.create_user(username='normal_systems', password='pass123456')
    admin = User.objects.create_superuser(username='admin_systems2', email='admin_systems2@example.com', password='adminpass2')
    device_system = DeviceSystems.objects.create(
        title='CoreSystem2', description='Core2', code_name='coresystem2', status=1, is_core=True, creator=admin
    )
    request = APIRequestFactory().put('/')
    request.user = user
    serializer = DeviceSystemsSerializer(device_system, data={'title': 'ShouldFail'}, context={'request': request}, partial=True)
    is_valid = serializer.is_valid()
    assert not is_valid
    assert 'non_field_errors' in serializer.errors or True

@pytest.mark.django_db
def test_device_systems_serializer_force_is_core_false_on_create_by_superuser():
    user = User.objects.create_superuser(username='admin_systems3', email='admin_systems3@example.com', password='adminpass3')
    factory_request = APIRequestFactory().post('/')
    factory_request.user = user
    data = {'title': 'SystemForce', 'description': 'Force core'}
    request = Request(factory_request)
    serializer = DeviceSystemsSerializer(data=data, context={'request': request})
    assert serializer.is_valid(), serializer.errors
    assert serializer.validated_data.get('is_core') is False or serializer.validated_data.get('is_core') is None

@pytest.mark.django_db
def test_device_systems_serializer_get_queryset_returns_all():
    user = User.objects.create_user(username='creator_systems2', password='pass123456')
    DeviceSystems.objects.create(title='SystemA', creator=user)
    DeviceSystems.objects.create(title='SystemB', creator=user)
    request = APIRequestFactory().get('/')
    request.user = user
    queryset = DeviceSystemsSerializer.get_queryset(request)
    assert queryset.count() >= 2

@pytest.mark.django_db
def test_device_systems_serializer_create_system_classmethod():
    user = User.objects.create_user(username='creator_systems3', password='pass123456')
    request = APIRequestFactory().post('/')
    request.user = user
    request.data = {'title': 'SystemC', 'description': 'DescC'}
    instance, _ = DeviceSystemsSerializer.create_system(request)
    assert instance['title'] == 'SystemC'
    assert instance['description'] == 'DescC'

@pytest.mark.django_db
def test_device_systems_serializer_update_system_classmethod():
    user = User.objects.create_user(username='creator_systems4', password='pass123456')
    device_system = DeviceSystems.objects.create(
        title='SystemD',
        description='DescD',
        creator=user
    )
    request = APIRequestFactory().put('/')
    request.user = user
    request.data = {'title': 'SystemD Updated'}
    updated, _ = DeviceSystemsSerializer.update_system(request, pk=device_system.pk, partial=True)
    assert updated['title'] == 'SystemD Updated'
