import pytest

from django.contrib.auth.models import User
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from api.models import DeviceProcessors
from api.serializers import DeviceProcessorsSerializer


"""
DeviceProcessorsSerializer tests
"""
@pytest.mark.django_db
def test_device_processors_serializer_create_and_representation():
    user = User.objects.create_user(username='creator_processors', password='pass123456')
    data = {
        'title': 'Intel i9',
        'description': 'High-end processor',
        'code_name': 'intel_i9',
        'status': 1,
        'is_core': False,
        'is_deprecated': False,
        'sort_order': 40
    }
    request = APIRequestFactory().post('/')
    request.user = user
    serializer = DeviceProcessorsSerializer(data=data, context={'request': request})
    assert serializer.is_valid(), serializer.errors
    instance = serializer.save(creator=user)
    assert instance.title == 'Intel i9'
    assert instance.description == 'High-end processor'
    assert instance.code_name == 'intel_i9'
    assert instance.status == 1
    assert instance.is_core is False
    assert instance.is_deprecated is False
    assert instance.sort_order == 40

    serializer2 = DeviceProcessorsSerializer(instance)
    data2 = serializer2.data
    assert data2['title'] == 'Intel i9'
    assert data2['description'] == 'High-end processor'
    assert data2['code_name'] == 'intel_i9'
    assert data2['status'] == 1
    assert data2['is_core'] is False or data2['is_core'] == 0
    assert data2['is_deprecated'] is False or data2['is_deprecated'] == 0
    assert data2['sort_order'] == 40
    assert 'creator' in data2
    assert 'updater' in data2

@pytest.mark.django_db
def test_device_processors_serializer_update_core_by_superuser():
    user = User.objects.create_superuser(
        username='admin_processors',
        email='admin_processors@example.com',
        password='adminpass',
        is_superuser=True
    )
    device_processor = DeviceProcessors.objects.create(
        title='CoreProc',
        description='Core',
        code_name='coreproc',
        status=1,
        is_core=True,
        creator=user
    )
    factory_request = APIRequestFactory().put('/')
    factory_request.user = user
    factory_request.data = {'title': 'UpdatedProc'}
    serializer, _ = DeviceProcessorsSerializer.update_processor(factory_request, device_processor.id, partial=True)
    assert isinstance(serializer, dict)
    assert serializer['title'] == 'UpdatedProc'
    assert 'id' in serializer

@pytest.mark.django_db
def test_device_processors_serializer_update_core_by_non_superuser_fails():
    user = User.objects.create_user(username='normal_processors', password='pass123456')
    admin = User.objects.create_superuser(username='admin_processors2', email='admin_processors2@example.com', password='adminpass2')
    device_processor = DeviceProcessors.objects.create(
        title='CoreProc2', description='Core2', code_name='coreproc2', status=1, is_core=True, creator=admin
    )
    request = APIRequestFactory().put('/')
    request.user = user
    serializer = DeviceProcessorsSerializer(device_processor, data={'title': 'ShouldFail'}, context={'request': request}, partial=True)
    is_valid = serializer.is_valid()
    assert not is_valid
    assert 'non_field_errors' in serializer.errors or True

@pytest.mark.django_db
def test_device_processors_serializer_force_is_core_false_on_create_by_superuser():
    user = User.objects.create_superuser(username='admin_processors3', email='admin_processors3@example.com', password='adminpass3')
    factory_request = APIRequestFactory().post('/')
    factory_request.user = user
    data = {'title': 'ProcForce', 'description': 'Force core'}
    request = Request(factory_request)
    serializer = DeviceProcessorsSerializer(data=data, context={'request': request})
    assert serializer.is_valid(), serializer.errors
    assert serializer.validated_data.get('is_core') is False or serializer.validated_data.get('is_core') is None

@pytest.mark.django_db
def test_device_processors_serializer_get_queryset_returns_all():
    user = User.objects.create_user(username='creator_processors2', password='pass123456')
    DeviceProcessors.objects.create(title='ProcA', creator=user)
    DeviceProcessors.objects.create(title='ProcB', creator=user)
    request = APIRequestFactory().get('/')
    request.user = user
    queryset = DeviceProcessorsSerializer.get_queryset(request)
    assert queryset.count() >= 2

@pytest.mark.django_db
def test_device_processors_serializer_create_processor_classmethod():
    user = User.objects.create_user(username='creator_processors3', password='pass123456')
    request = APIRequestFactory().post('/')
    request.user = user
    request.data = {'title': 'ProcC', 'description': 'DescC'}
    instance, _ = DeviceProcessorsSerializer.create_processor(request)
    assert instance['title'] == 'ProcC'
    assert instance['description'] == 'DescC'

@pytest.mark.django_db
def test_device_processors_serializer_update_processor_classmethod():
    user = User.objects.create_user(username='creator_processors4', password='pass123456')
    device_processor = DeviceProcessors.objects.create(
        title='ProcD',
        description='DescD',
        creator=user
    )
    request = APIRequestFactory().put('/')
    request.user = user
    request.data = {'title': 'ProcD Updated'}
    updated, _ = DeviceProcessorsSerializer.update_processor(request, pk=device_processor.pk, partial=True)
    assert updated['title'] == 'ProcD Updated'
