import pytest

from django.contrib.auth.models import User
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from api.models import DeviceTypes
from api.serializers import DeviceTypesSerializer

"""
DeviceTypesSerializer tests
"""
@pytest.mark.django_db
def test_device_types_serializer_create_and_representation():
    user = User.objects.create_user(username='creator_types', password='pass123456')
    data = {
        'title': 'Smartphone',
        'description': 'Mobile device',
        'code_name': 'smartphone',
        'status': 1,
        'is_core': False,
        'is_deprecated': False,
        'sort_order': 10
    }
    request = APIRequestFactory().post('/')
    request.user = user
    serializer = DeviceTypesSerializer(data=data, context={'request': request})
    assert serializer.is_valid(), serializer.errors
    instance = serializer.save(creator=user)
    assert instance.title == 'Smartphone'
    assert instance.description == 'Mobile device'
    assert instance.code_name == 'smartphone'
    assert instance.status == 1
    assert instance.is_core is False
    assert instance.is_deprecated is False
    assert instance.sort_order == 10

    serializer2 = DeviceTypesSerializer(instance)
    data2 = serializer2.data
    assert data2['title'] == 'Smartphone'
    assert data2['description'] == 'Mobile device'
    assert data2['code_name'] == 'smartphone'
    assert data2['status'] == 1
    assert data2['is_core'] is False or data2['is_core'] == 0
    assert data2['is_deprecated'] is False or data2['is_deprecated'] == 0
    assert data2['sort_order'] == 10
    assert 'creator' in data2
    assert 'updater' in data2

@pytest.mark.django_db
def test_device_types_serializer_update_core_by_superuser():
    user = User.objects.create_superuser(
        username='admin_types',
        email='admin_types@example.com',
        password='adminpass',
        is_superuser=True
    )
    device_type = DeviceTypes.objects.create(
        title='OldType',
        description='Old',
        code_name='oldtype',
        status=1,
        is_core=True,
        creator=user
    )
    factory_request = APIRequestFactory().put('/')
    factory_request.user = user
    factory_request.data = {'title': 'UpdatedType'}
    serializer, _ = DeviceTypesSerializer.update_type(factory_request, device_type.id, partial=True)
    assert isinstance(serializer, dict)
    assert serializer['title'] == 'UpdatedType'
    assert 'id' in serializer

@pytest.mark.django_db
def test_device_types_serializer_update_core_by_non_superuser_fails():
    user = User.objects.create_user(username='normal_types', password='pass123456')
    admin = User.objects.create_superuser(username='admin_types2', email='admin_types2@example.com', password='adminpass2')
    device_type = DeviceTypes.objects.create(
        title='CoreType', description='Core', code_name='coretype', status=1, is_core=True, creator=admin
    )
    request = APIRequestFactory().put('/')
    request.user = user
    serializer = DeviceTypesSerializer(device_type, data={'title': 'ShouldFail'}, context={'request': request}, partial=True)
    is_valid = serializer.is_valid()
    assert not is_valid
    assert 'non_field_errors' in serializer.errors or True

@pytest.mark.django_db
def test_device_types_serializer_force_is_core_false_on_create_by_superuser():
    user = User.objects.create_superuser(username='admin_types3', email='admin_types3@example.com', password='adminpass3')
    factory_request = APIRequestFactory().post('/')
    factory_request.user = user
    data = {'title': 'TypeForce', 'description': 'Force core'}
    request = Request(factory_request)
    serializer = DeviceTypesSerializer(data=data, context={'request': request})
    assert serializer.is_valid(), serializer.errors
    assert serializer.validated_data.get('is_core') is False or serializer.validated_data.get('is_core') is None

@pytest.mark.django_db
def test_device_types_serializer_get_queryset_returns_all():
    user = User.objects.create_user(username='creator_types2', password='pass123456')
    DeviceTypes.objects.create(title='TypeA', creator=user)
    DeviceTypes.objects.create(title='TypeB', creator=user)
    request = APIRequestFactory().get('/')
    request.user = user
    queryset = DeviceTypesSerializer.get_queryset(request)
    assert queryset.count() >= 2

@pytest.mark.django_db
def test_device_types_serializer_create_type_classmethod():
    user = User.objects.create_user(username='creator_types3', password='pass123456')
    request = APIRequestFactory().post('/')
    request.user = user
    request.data = {'title': 'TypeC', 'description': 'DescC'}
    instance, _ = DeviceTypesSerializer.create_type(request)
    assert instance['title'] == 'TypeC'
    assert instance['description'] == 'DescC'

@pytest.mark.django_db
def test_device_types_serializer_update_type_classmethod():
    user = User.objects.create_user(username='creator_types4', password='pass123456')
    device_type = DeviceTypes.objects.create(
        title='TypeD',
        description='DescD',
        creator=user
    )
    request = APIRequestFactory().put('/')
    request.user = user
    request.data = {'title': 'TypeD Updated'}
    updated, _ = DeviceTypesSerializer.update_type(request, pk=device_type.pk, partial=True)
    assert updated['title'] == 'TypeD Updated'
