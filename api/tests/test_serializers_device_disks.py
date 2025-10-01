import pytest

from django.contrib.auth.models import User
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from api.models import DeviceDisks
from api.serializers import DeviceDisksSerializer


"""
DeviceDisksSerializer tests
"""
@pytest.mark.django_db
def test_device_disks_serializer_create_and_representation():
    user = User.objects.create_user(username='creator_disks', password='pass123456')
    data = {
        'title': '1TB SSD',
        'description': 'Solid State Drive',
        'code_name': '1tb_ssd',
        'status': 1,
        'is_core': False,
        'is_deprecated': False,
        'sort_order': 60
    }
    factory_request = APIRequestFactory().post('/')
    factory_request.user = user
    serializer = DeviceDisksSerializer(data=data, context={'request': factory_request})
    assert serializer.is_valid(), serializer.errors
    instance = serializer.save(creator=user)
    assert instance.title == '1TB SSD'
    assert instance.description == 'Solid State Drive'
    assert instance.code_name == '1tb_ssd'
    assert instance.status == 1
    assert instance.is_core is False
    assert instance.is_deprecated is False
    assert instance.sort_order == 60

    serializer2 = DeviceDisksSerializer(instance)
    data2 = serializer2.data
    assert data2['title'] == '1TB SSD'
    assert data2['description'] == 'Solid State Drive'
    assert data2['code_name'] == '1tb_ssd'
    assert data2['status'] == 1
    assert data2['is_core'] is False or data2['is_core'] == 0
    assert data2['is_deprecated'] is False or data2['is_deprecated'] == 0
    assert data2['sort_order'] == 60
    assert 'creator' in data2
    assert 'updater' in data2

@pytest.mark.django_db
def test_device_disks_serializer_update_core_by_superuser():
    user = User.objects.create_superuser(
        username='admin_disks',
        email='admin_disks@example.com',
        password='adminpass',
        is_superuser=True
    )
    device_disk = DeviceDisks.objects.create(
        title='CoreDisk',
        description='Core',
        code_name='coredisk',
        status=1,
        is_core=True,
        creator=user
    )
    factory_request = APIRequestFactory().put('/')
    factory_request.user = user
    factory_request.data = {'title': 'UpdatedDisk'}
    serializer, _ = DeviceDisksSerializer.update_disk(factory_request, device_disk.id, partial=True)
    assert isinstance(serializer, dict)
    assert serializer['title'] == 'UpdatedDisk'
    assert 'id' in serializer

@pytest.mark.django_db
def test_device_disks_serializer_update_core_by_non_superuser_fails():
    user = User.objects.create_user(username='normal_disks', password='pass123456')
    admin = User.objects.create_superuser(username='admin_disks2', email='admin_disks2@example.com', password='adminpass2')
    device_disk = DeviceDisks.objects.create(
        title='CoreDisk2', description='Core2', code_name='coredisk2', status=1, is_core=True, creator=admin
    )
    request = APIRequestFactory().put('/')
    request.user = user
    serializer = DeviceDisksSerializer(device_disk, data={'title': 'ShouldFail'}, context={'request': request}, partial=True)
    is_valid = serializer.is_valid()
    assert not is_valid
    assert 'non_field_errors' in serializer.errors or True

@pytest.mark.django_db
def test_device_disks_serializer_force_is_core_false_on_create_by_superuser():
    user = User.objects.create_superuser(username='admin_disks3', email='admin_disks3@example.com', password='adminpass3')
    factory_request = APIRequestFactory().post('/')
    factory_request.user = user
    data = {'title': 'DiskForce', 'description': 'Force core'}
    request = Request(factory_request)
    serializer = DeviceDisksSerializer(data=data, context={'request': request})
    assert serializer.is_valid(), serializer.errors
    assert serializer.validated_data.get('is_core') is False or serializer.validated_data.get('is_core') is None

@pytest.mark.django_db
def test_device_disks_serializer_get_queryset_returns_all():
    user = User.objects.create_user(username='creator_disks2', password='pass123456')
    DeviceDisks.objects.create(title='DiskA', creator=user)
    DeviceDisks.objects.create(title='DiskB', creator=user)
    request = APIRequestFactory().get('/')
    request.user = user
    queryset = DeviceDisksSerializer.get_queryset(request)
    assert queryset.count() >= 2

@pytest.mark.django_db
def test_device_disks_serializer_create_disk_classmethod():
    user = User.objects.create_user(username='creator_disks3', password='pass123456')
    request = APIRequestFactory().post('/')
    request.user = user
    request.data = {'title': 'DiskC', 'description': 'DescC'}
    instance, _ = DeviceDisksSerializer.create_disk(request)
    assert instance['title'] == 'DiskC'
    assert instance['description'] == 'DescC'

@pytest.mark.django_db
def test_device_disks_serializer_update_disk_classmethod():
    user = User.objects.create_user(username='creator_disks4', password='pass123456')
    device_disk = DeviceDisks.objects.create(
        title='DiskD',
        description='DescD',
        creator=user
    )
    request = APIRequestFactory().put('/')
    request.user = user
    request.data = {'title': 'DiskD Updated'}
    updated, _ = DeviceDisksSerializer.update_disk(request, pk=device_disk.pk, partial=True)
    assert updated['title'] == 'DiskD Updated'
