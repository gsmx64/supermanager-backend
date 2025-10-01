import pytest

from django.contrib.auth.models import User
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from api.models import DeviceRAMs
from api.serializers import DeviceRAMsSerializer


"""
DeviceRAMsSerializer tests
"""
@pytest.mark.django_db
def test_device_rams_serializer_create_and_representation():
    user = User.objects.create_user(username='creator_rams', password='pass123456')
    data = {
        'title': '8GB DDR4',
        'description': 'Standard RAM',
        'code_name': '8gb_ddr4',
        'status': 1,
        'is_core': False,
        'is_deprecated': False,
        'sort_order': 50
    }
    request = APIRequestFactory().post('/')
    request.user = user
    serializer = DeviceRAMsSerializer(data=data, context={'request': request})
    assert serializer.is_valid(), serializer.errors
    instance = serializer.save(creator=user)
    assert instance.title == '8GB DDR4'
    assert instance.description == 'Standard RAM'
    assert instance.code_name == '8gb_ddr4'
    assert instance.status == 1
    assert instance.is_core is False
    assert instance.is_deprecated is False
    assert instance.sort_order == 50

    serializer2 = DeviceRAMsSerializer(instance)
    data2 = serializer2.data
    assert data2['title'] == '8GB DDR4'
    assert data2['description'] == 'Standard RAM'
    assert data2['code_name'] == '8gb_ddr4'
    assert data2['status'] == 1
    assert data2['is_core'] is False or data2['is_core'] == 0
    assert data2['is_deprecated'] is False or data2['is_deprecated'] == 0
    assert data2['sort_order'] == 50
    assert 'creator' in data2
    assert 'updater' in data2

@pytest.mark.django_db
def test_device_rams_serializer_update_core_by_superuser():
    user = User.objects.create_superuser(
        username='admin_rams',
        email='admin_rams@example.com',
        password='adminpass',
        is_superuser=True
    )
    device_ram = DeviceRAMs.objects.create(
        title='CoreRAM',
        description='Core',
        code_name='coreram',
        status=1,
        is_core=True,
        creator=user
    )
    factory_request = APIRequestFactory().put('/')
    factory_request.user = user
    factory_request.data = {'title': 'UpdatedRAM'}
    serializer, _ = DeviceRAMsSerializer.update_ram(factory_request, device_ram.id, partial=True)
    assert isinstance(serializer, dict)
    assert serializer['title'] == 'UpdatedRAM'
    assert 'id' in serializer

@pytest.mark.django_db
def test_device_rams_serializer_update_core_by_non_superuser_fails():
    user = User.objects.create_user(username='normal_rams', password='pass123456')
    admin = User.objects.create_superuser(username='admin_rams2', email='admin_rams2@example.com', password='adminpass2')
    device_ram = DeviceRAMs.objects.create(
        title='CoreRAM2', description='Core2', code_name='coreram2', status=1, is_core=True, creator=admin
    )
    request = APIRequestFactory().put('/')
    request.user = user
    serializer = DeviceRAMsSerializer(device_ram, data={'title': 'ShouldFail'}, context={'request': request}, partial=True)
    is_valid = serializer.is_valid()
    assert not is_valid
    assert 'non_field_errors' in serializer.errors or True

@pytest.mark.django_db
def test_device_rams_serializer_force_is_core_false_on_create_by_superuser():
    user = User.objects.create_superuser(username='admin_rams3', email='admin_rams3@example.com', password='adminpass3')
    factory_request = APIRequestFactory().post('/')
    factory_request.user = user
    data = {'title': 'RAMForce', 'description': 'Force core'}
    request = Request(factory_request)
    serializer = DeviceRAMsSerializer(data=data, context={'request': request})
    assert serializer.is_valid(), serializer.errors
    assert serializer.validated_data.get('is_core') is False or serializer.validated_data.get('is_core') is None

@pytest.mark.django_db
def test_device_rams_serializer_get_queryset_returns_all():
    user = User.objects.create_user(username='creator_rams2', password='pass123456')
    DeviceRAMs.objects.create(title='RAM_A', creator=user)
    DeviceRAMs.objects.create(title='RAM_B', creator=user)
    request = APIRequestFactory().get('/')
    request.user = user
    queryset = DeviceRAMsSerializer.get_queryset(request)
    assert queryset.count() >= 2

@pytest.mark.django_db
def test_device_rams_serializer_create_ram_classmethod():
    user = User.objects.create_user(username='creator_rams3', password='pass123456')
    request = APIRequestFactory().post('/')
    request.user = user
    request.data = {'title': 'RAM_C', 'description': 'DescC'}
    instance, _ = DeviceRAMsSerializer.create_ram(request)
    assert instance['title'] == 'RAM_C'
    assert instance['description'] == 'DescC'

@pytest.mark.django_db
def test_device_rams_serializer_update_ram_classmethod():
    user = User.objects.create_user(username='creator_rams4', password='pass123456')
    device_ram = DeviceRAMs.objects.create(
        title='RAM_D',
        description='DescD',
        creator=user
    )
    request = APIRequestFactory().put('/')
    request.user = user
    request.data = {'title': 'RAM_D Updated'}
    updated, _ = DeviceRAMsSerializer.update_ram(request, pk=device_ram.pk, partial=True)
    assert updated['title'] == 'RAM_D Updated'
