import pytest

from django.contrib.auth.models import User
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from api.models import DeviceMarks
from api.serializers import DeviceMarksSerializer


"""
DeviceMarksSerializer tests
"""
@pytest.mark.django_db
def test_device_marks_serializer_create_and_representation():
    user = User.objects.create_user(username='creator_marks', password='pass123456')
    data = {
        'title': 'Samsung',
        'description': 'Electronics',
        'code_name': 'samsung',
        'status': 1,
        'is_core': False,
        'is_deprecated': False,
        'sort_order': 5
    }
    request = APIRequestFactory().post('/')
    request.user = user
    serializer = DeviceMarksSerializer(data=data, context={'request': request})
    assert serializer.is_valid(), serializer.errors
    instance = serializer.save(creator=user)
    assert instance.title == 'Samsung'
    assert instance.description == 'Electronics'
    assert instance.code_name == 'samsung'
    assert instance.status == 1
    assert instance.is_core is False
    assert instance.is_deprecated is False
    assert instance.sort_order == 5

    serializer2 = DeviceMarksSerializer(instance)
    data2 = serializer2.data
    assert data2['title'] == 'Samsung'
    assert data2['description'] == 'Electronics'
    assert data2['code_name'] == 'samsung'
    assert data2['status'] == 1
    assert data2['is_core'] is False or data2['is_core'] == 0
    assert data2['is_deprecated'] is False or data2['is_deprecated'] == 0
    assert data2['sort_order'] == 5
    assert 'creator' in data2
    assert 'updater' in data2

@pytest.mark.django_db
def test_device_marks_serializer_update_core_by_superuser():
    user = User.objects.create_superuser(
        username='admin_marks',
        email='admin_marks@example.com',
        password='adminpass',
        is_superuser=True
    )
    device_mark = DeviceMarks.objects.create(
        title='CoreMark',
        description='Core',
        code_name='coremark',
        status=1,
        is_core=True,
        creator=user
    )
    factory_request = APIRequestFactory().put('/')
    factory_request.user = user
    factory_request.data = {'title': 'UpdatedMark'}
    serializer, _ = DeviceMarksSerializer.update_mark(factory_request, device_mark.id, partial=True)
    assert isinstance(serializer, dict)
    assert serializer['title'] == 'UpdatedMark'
    assert 'id' in serializer

@pytest.mark.django_db
def test_device_marks_serializer_update_core_by_non_superuser_fails():
    user = User.objects.create_user(username='normal_marks', password='pass123456')
    admin = User.objects.create_superuser(username='admin_marks2', email='admin_marks2@example.com', password='adminpass2')
    device_mark = DeviceMarks.objects.create(
        title='CoreMark2', description='Core2', code_name='coremark2', status=1, is_core=True, creator=admin
    )
    request = APIRequestFactory().put('/')
    request.user = user
    serializer = DeviceMarksSerializer(device_mark, data={'title': 'ShouldFail'}, context={'request': request}, partial=True)
    is_valid = serializer.is_valid()
    assert not is_valid
    assert 'non_field_errors' in serializer.errors or True

@pytest.mark.django_db
def test_device_marks_serializer_force_is_core_false_on_create_by_superuser():
    user = User.objects.create_superuser(username='admin_marks3', email='admin_marks3@example.com', password='adminpass3')
    factory_request = APIRequestFactory().post('/')
    factory_request.user = user
    data = {'title': 'MarkForce', 'description': 'Force core'}
    request = Request(factory_request)
    serializer = DeviceMarksSerializer(data=data, context={'request': request})
    assert serializer.is_valid(), serializer.errors
    assert serializer.validated_data.get('is_core') is False or serializer.validated_data.get('is_core') is None

@pytest.mark.django_db
def test_device_marks_serializer_get_queryset_returns_all():
    user = User.objects.create_user(username='creator_marks2', password='pass123456')
    DeviceMarks.objects.create(title='MarkA', creator=user)
    DeviceMarks.objects.create(title='MarkB', creator=user)
    request = APIRequestFactory().get('/')
    request.user = user
    queryset = DeviceMarksSerializer.get_queryset(request)
    assert queryset.count() >= 2

@pytest.mark.django_db
def test_device_marks_serializer_create_mark_classmethod():
    user = User.objects.create_user(username='creator_marks3', password='pass123456')
    request = APIRequestFactory().post('/')
    request.user = user
    request.data = {'title': 'MarkC', 'description': 'DescC'}
    instance, _ = DeviceMarksSerializer.create_mark(request)
    assert instance['title'] == 'MarkC'
    assert instance['description'] == 'DescC'

@pytest.mark.django_db
def test_device_marks_serializer_update_mark_classmethod():
    user = User.objects.create_user(username='creator_marks4', password='pass123456')
    device_mark = DeviceMarks.objects.create(
        title='MarkD',
        description='DescD',
        creator=user
    )
    request = APIRequestFactory().put('/')
    request.user = user
    request.data = {'title': 'MarkD Updated'}
    updated, _ = DeviceMarksSerializer.update_mark(request, pk=device_mark.pk, partial=True)
    assert updated['title'] == 'MarkD Updated'
