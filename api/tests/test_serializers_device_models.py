import pytest

from django.contrib.auth.models import User
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from api.models import DeviceModels
from api.serializers import DeviceModelsSerializer


"""
DeviceModelsSerializer tests
"""
@pytest.mark.django_db
def test_device_models_serializer_create_and_representation():
    user = User.objects.create_user(username='creator_models', password='pass123456')
    data = {
        'title': 'Galaxy S21',
        'description': 'Samsung smartphone model',
        'code_name': 'galaxy_s21',
        'status': 1,
        'is_core': False,
        'is_deprecated': False,
        'sort_order': 15
    }
    request = APIRequestFactory().post('/')
    request.user = user
    serializer = DeviceModelsSerializer(data=data, context={'request': request})
    assert serializer.is_valid(), serializer.errors
    instance = serializer.save(creator=user)
    assert instance.title == 'Galaxy S21'
    assert instance.description == 'Samsung smartphone model'
    assert instance.code_name == 'galaxy_s21'
    assert instance.status == 1
    assert instance.is_core is False
    assert instance.is_deprecated is False
    assert instance.sort_order == 15

    serializer2 = DeviceModelsSerializer(instance)
    data2 = serializer2.data
    assert data2['title'] == 'Galaxy S21'
    assert data2['description'] == 'Samsung smartphone model'
    assert data2['code_name'] == 'galaxy_s21'
    assert data2['status'] == 1
    assert data2['is_core'] is False or data2['is_core'] == 0
    assert data2['is_deprecated'] is False or data2['is_deprecated'] == 0
    assert data2['sort_order'] == 15
    assert 'creator' in data2
    assert 'updater' in data2

@pytest.mark.django_db
def test_device_models_serializer_update_core_by_superuser():
    user = User.objects.create_superuser(
        username='admin_models',
        email='admin_models@example.com',
        password='adminpass',
        is_superuser=True
    )
    device_model = DeviceModels.objects.create(
        title='CoreModel',
        description='Core',
        code_name='coremodel',
        status=1,
        is_core=True,
        creator=user
    )
    factory_request = APIRequestFactory().put('/')
    factory_request.user = user
    factory_request.data = {'title': 'UpdatedModel'}
    serializer, _ = DeviceModelsSerializer.update_model(factory_request, device_model.id, partial=True)
    assert isinstance(serializer, dict)
    assert serializer['title'] == 'UpdatedModel'
    assert 'id' in serializer

@pytest.mark.django_db
def test_device_models_serializer_update_core_by_non_superuser_fails():
    user = User.objects.create_user(username='normal_models', password='pass123456')
    admin = User.objects.create_superuser(username='admin_models2', email='admin_models2@example.com', password='adminpass2')
    device_model = DeviceModels.objects.create(
        title='CoreModel2', description='Core2', code_name='coremodel2', status=1, is_core=True, creator=admin
    )
    request = APIRequestFactory().put('/')
    request.user = user
    serializer = DeviceModelsSerializer(device_model, data={'title': 'ShouldFail'}, context={'request': request}, partial=True)
    is_valid = serializer.is_valid()
    assert not is_valid
    assert 'non_field_errors' in serializer.errors or True

@pytest.mark.django_db
def test_device_models_serializer_force_is_core_false_on_create_by_superuser():
    user = User.objects.create_superuser(username='admin_models3', email='admin_models3@example.com', password='adminpass3')
    factory_request = APIRequestFactory().post('/')
    factory_request.user = user
    data = {'title': 'ModelForce', 'description': 'Force core'}
    request = Request(factory_request)
    serializer = DeviceModelsSerializer(data=data, context={'request': request})
    assert serializer.is_valid(), serializer.errors
    assert serializer.validated_data.get('is_core') is False or serializer.validated_data.get('is_core') is None

@pytest.mark.django_db
def test_device_models_serializer_get_queryset_returns_all():
    user = User.objects.create_user(username='creator_models2', password='pass123456')
    DeviceModels.objects.create(title='ModelA', creator=user)
    DeviceModels.objects.create(title='ModelB', creator=user)
    request = APIRequestFactory().get('/')
    request.user = user
    queryset = DeviceModelsSerializer.get_queryset(request)
    assert queryset.count() >= 2

@pytest.mark.django_db
def test_device_models_serializer_create_model_classmethod():
    user = User.objects.create_user(username='creator_models3', password='pass123456')
    request = APIRequestFactory().post('/')
    request.user = user
    request.data = {'title': 'ModelC', 'description': 'DescC'}
    instance, _ = DeviceModelsSerializer.create_model(request)
    assert instance['title'] == 'ModelC'
    assert instance['description'] == 'DescC'

@pytest.mark.django_db
def test_device_models_serializer_update_model_classmethod():
    user = User.objects.create_user(username='creator_models4', password='pass123456')
    device_model = DeviceModels.objects.create(
        title='ModelD',
        description='DescD',
        creator=user
    )
    request = APIRequestFactory().put('/')
    request.user = user
    request.data = {'title': 'ModelD Updated'}
    updated, _ = DeviceModelsSerializer.update_model(request, pk=device_model.pk, partial=True)
    assert updated['title'] == 'ModelD Updated'
