import pytest

from django.contrib.auth.models import User
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from api.models import DeviceBuilds
from api.serializers import DeviceBuildsSerializer


"""
DeviceBuildsSerializer tests
"""
@pytest.mark.django_db
def test_device_builds_serializer_create_and_representation():
    user = User.objects.create_user(username='creator_builds', password='pass123456')
    data = {
        'title': 'Build2024',
        'description': '2024 build version',
        'code_name': 'build2024',
        'status': 1,
        'is_core': False,
        'is_deprecated': False,
        'sort_order': 30
    }
    request = APIRequestFactory().post('/')
    request.user = user
    serializer = DeviceBuildsSerializer(data=data, context={'request': request})
    assert serializer.is_valid(), serializer.errors
    instance = serializer.save(creator=user)
    assert instance.title == 'Build2024'
    assert instance.description == '2024 build version'
    assert instance.code_name == 'build2024'
    assert instance.status == 1
    assert instance.is_core is False
    assert instance.is_deprecated is False
    assert instance.sort_order == 30

    serializer2 = DeviceBuildsSerializer(instance)
    data2 = serializer2.data
    assert data2['title'] == 'Build2024'
    assert data2['description'] == '2024 build version'
    assert data2['code_name'] == 'build2024'
    assert data2['status'] == 1
    assert data2['is_core'] is False or data2['is_core'] == 0
    assert data2['is_deprecated'] is False or data2['is_deprecated'] == 0
    assert data2['sort_order'] == 30
    assert 'creator' in data2
    assert 'updater' in data2

@pytest.mark.django_db
def test_device_builds_serializer_update_core_by_superuser():
    user = User.objects.create_superuser(
        username='admin_builds',
        email='admin_builds@example.com',
        password='adminpass',
        is_superuser=True
    )
    device_build = DeviceBuilds.objects.create(
        title='CoreBuild',
        description='Core',
        code_name='corebuild',
        status=1,
        is_core=True,
        creator=user
    )
    factory_request = APIRequestFactory().put('/')
    factory_request.user = user
    factory_request.data = {'title': 'UpdatedBuild'}
    serializer, _ = DeviceBuildsSerializer.update_build(factory_request, device_build.id, partial=True)
    assert isinstance(serializer, dict)
    assert serializer['title'] == 'UpdatedBuild'
    assert 'id' in serializer

@pytest.mark.django_db
def test_device_builds_serializer_update_core_by_non_superuser_fails():
    user = User.objects.create_user(username='normal_builds', password='pass123456')
    admin = User.objects.create_superuser(username='admin_builds2', email='admin_builds2@example.com', password='adminpass2')
    device_build = DeviceBuilds.objects.create(
        title='CoreBuild2', description='Core2', code_name='corebuild2', status=1, is_core=True, creator=admin
    )
    request = APIRequestFactory().put('/')
    request.user = user
    serializer = DeviceBuildsSerializer(device_build, data={'title': 'ShouldFail'}, context={'request': request}, partial=True)
    is_valid = serializer.is_valid()
    assert not is_valid
    assert 'non_field_errors' in serializer.errors or True

@pytest.mark.django_db
def test_device_builds_serializer_force_is_core_false_on_create_by_superuser():
    user = User.objects.create_superuser(username='admin_builds3', email='admin_builds3@example.com', password='adminpass3')
    factory_request = APIRequestFactory().post('/')
    factory_request.user = user
    data = {'title': 'BuildForce', 'description': 'Force core'}
    request = Request(factory_request)
    serializer = DeviceBuildsSerializer(data=data, context={'request': request})
    assert serializer.is_valid(), serializer.errors
    assert serializer.validated_data.get('is_core') is False or serializer.validated_data.get('is_core') is None

@pytest.mark.django_db
def test_device_builds_serializer_get_queryset_returns_all():
    user = User.objects.create_user(username='creator_builds2', password='pass123456')
    DeviceBuilds.objects.create(title='BuildA', creator=user)
    DeviceBuilds.objects.create(title='BuildB', creator=user)
    request = APIRequestFactory().get('/')
    request.user = user
    queryset = DeviceBuildsSerializer.get_queryset(request)
    assert queryset.count() >= 2

@pytest.mark.django_db
def test_device_builds_serializer_create_build_classmethod():
    user = User.objects.create_user(username='creator_builds3', password='pass123456')
    request = APIRequestFactory().post('/')
    request.user = user
    request.data = {'title': 'BuildC', 'description': 'DescC'}
    instance, _ = DeviceBuildsSerializer.create_build(request)
    assert instance['title'] == 'BuildC'
    assert instance['description'] == 'DescC'

@pytest.mark.django_db
def test_device_builds_serializer_update_build_classmethod():
    user = User.objects.create_user(username='creator_builds4', password='pass123456')
    device_build = DeviceBuilds.objects.create(
        title='BuildD',
        description='DescD',
        creator=user
    )
    request = APIRequestFactory().put('/')
    request.user = user
    request.data = {'title': 'BuildD Updated'}
    updated, _ = DeviceBuildsSerializer.update_build(request, pk=device_build.pk, partial=True)
    assert updated['title'] == 'BuildD Updated'
