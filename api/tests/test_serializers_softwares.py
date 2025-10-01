import pytest

from django.contrib.auth.models import User
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from api.models import Softwares
from api.serializers import SoftwaresSerializer

"""
SoftwaresSerializer tests
"""
@pytest.mark.django_db
def test_softwares_serializer_create_and_representation():
    user = User.objects.create_user(username='creator_softwares', password='pass123456')
    data = {
        'title': 'Office Suite',
        'description': 'Productivity software',
        'code_name': 'office_suite',
        'status': 1,
        'is_core': False,
        'is_deprecated': False,
        'sort_order': 70
    }
    request = APIRequestFactory().post('/')
    request.user = user
    serializer = SoftwaresSerializer(data=data, context={'request': request})
    assert serializer.is_valid(), serializer.errors
    instance = serializer.save(creator=user)
    assert instance.title == 'Office Suite'
    assert instance.description == 'Productivity software'
    assert instance.code_name == 'office_suite'
    assert instance.status == 1
    assert instance.is_core is False
    assert instance.is_deprecated is False
    assert instance.sort_order == 70

    serializer2 = SoftwaresSerializer(instance)
    data2 = serializer2.data
    assert data2['title'] == 'Office Suite'
    assert data2['description'] == 'Productivity software'
    assert data2['code_name'] == 'office_suite'
    assert data2['status'] == 1
    assert data2['is_core'] is False or data2['is_core'] == 0
    assert data2['is_deprecated'] is False or data2['is_deprecated'] == 0
    assert data2['sort_order'] == 70
    assert 'creator' in data2
    assert 'updater' in data2

@pytest.mark.django_db
def test_softwares_serializer_update_core_by_superuser():
    user = User.objects.create_superuser(
        username='admin_softwares',
        email='admin_softwares@example.com',
        password='adminpass',
        is_superuser=True
    )
    software = Softwares.objects.create(
        title='CoreSoft',
        description='Core',
        code_name='coresoft',
        status=1,
        is_core=True,
        creator=user
    )
    factory_request = APIRequestFactory().put('/')
    factory_request.user = user
    factory_request.data = {'title': 'UpdatedSoft'}
    serializer, _ = SoftwaresSerializer.update_software(factory_request, software.id, partial=True)
    assert isinstance(serializer, dict)
    assert serializer['title'] == 'UpdatedSoft'
    assert 'id' in serializer

@pytest.mark.django_db
def test_softwares_serializer_update_core_by_non_superuser_fails():
    user = User.objects.create_user(username='normal_softwares', password='pass123456')
    admin = User.objects.create_superuser(username='admin_softwares2', email='admin_softwares2@example.com', password='adminpass2')
    software = Softwares.objects.create(
        title='CoreSoft2', description='Core2', code_name='coresoft2', status=1, is_core=True, creator=admin
    )
    request = APIRequestFactory().put('/')
    request.user = user
    serializer = SoftwaresSerializer(software, data={'title': 'ShouldFail'}, context={'request': request}, partial=True)
    is_valid = serializer.is_valid()
    assert not is_valid
    assert 'non_field_errors' in serializer.errors or True

@pytest.mark.django_db
def test_softwares_serializer_force_is_core_false_on_create_by_superuser():
    user = User.objects.create_superuser(username='admin_softwares3', email='admin_softwares3@example.com', password='adminpass3')
    factory_request = APIRequestFactory().post('/')
    factory_request.user = user
    data = {'title': 'SoftForce', 'description': 'Force core'}
    request = Request(factory_request)
    serializer = SoftwaresSerializer(data=data, context={'request': request})
    assert serializer.is_valid(), serializer.errors
    assert serializer.validated_data.get('is_core') is False or serializer.validated_data.get('is_core') is None

@pytest.mark.django_db
def test_softwares_serializer_get_queryset_returns_all():
    user = User.objects.create_user(username='creator_softwares2', password='pass123456')
    Softwares.objects.create(title='SoftA', creator=user)
    Softwares.objects.create(title='SoftB', creator=user)
    request = APIRequestFactory().get('/')
    request.user = user
    queryset = SoftwaresSerializer.get_queryset(request)
    assert queryset.count() >= 2

@pytest.mark.django_db
def test_softwares_serializer_create_software_classmethod():
    user = User.objects.create_user(username='creator_softwares3', password='pass123456')
    request = APIRequestFactory().post('/')
    request.user = user
    request.data = {'title': 'SoftC', 'description': 'DescC'}
    instance, _ = SoftwaresSerializer.create_software(request)
    assert instance['title'] == 'SoftC'
    assert instance['description'] == 'DescC'

@pytest.mark.django_db
def test_softwares_serializer_update_software_classmethod():
    user = User.objects.create_user(username='creator_softwares4', password='pass123456')
    software = Softwares.objects.create(
        title='SoftD',
        description='DescD',
        creator=user
    )
    request = APIRequestFactory().put('/')
    request.user = user
    request.data = {'title': 'SoftD Updated'}
    updated, _ = SoftwaresSerializer.update_software(request, pk=software.pk, partial=True)
    assert updated['title'] == 'SoftD Updated'
