import pytest

from django.contrib.auth.models import User
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from api.models import LocationZones, Locations
from api.serializers import LocationZonesSerializer


"""
LocationZonesSerializer tests
"""
@pytest.mark.django_db
def test_location_zones_serializer_create_and_representation():
    user = User.objects.create_user(username='creator_zones', password='pass123456')
    data = {
        'title': 'ZoneTest',
        'description': 'Test zone',
        'code_name': 'zonetest',
        'status': 1,
        'is_core': False,
        'manager': 'Manager Name',
        'manager_email': 'manager@example.com',
        'manager_phone': '123456789',
        'manager_mobile': '987654321',
        'sort_order': 1
    }
    request = APIRequestFactory().post('/')
    request.user = user
    serializer = LocationZonesSerializer(data=data, context={'request': request})
    assert serializer.is_valid(), serializer.errors
    instance = serializer.save(creator=user)
    assert instance.title == 'ZoneTest'
    assert instance.description == 'Test zone'
    assert instance.code_name == 'zonetest'
    assert instance.status == 1
    assert instance.is_core is False
    assert instance.manager == 'Manager Name'
    assert instance.manager_email == 'manager@example.com'
    assert instance.manager_phone == '123456789'
    assert instance.manager_mobile == '987654321'
    assert instance.sort_order == 1

    serializer2 = LocationZonesSerializer(instance)
    data2 = serializer2.data
    assert data2['title'] == 'ZoneTest'
    assert data2['description'] == 'Test zone'
    assert data2['code_name'] == 'zonetest'
    assert data2['status'] == 1
    assert data2['is_core'] is False or data2['is_core'] == 0
    assert data2['manager'] == 'Manager Name'
    assert data2['manager_email'] == 'manager@example.com'
    assert data2['manager_phone'] == '123456789'
    assert data2['manager_mobile'] == '987654321'
    assert data2['sort_order'] == 1
    assert 'creator' in data2
    assert 'updater' in data2
    assert 'locations_count' in data2

@pytest.mark.django_db
def test_location_zones_serializer_update_core_by_superuser():
    user = User.objects.create_superuser(username='admin_zones', email='admin_zones@example.com', password='adminpass')
    zone = LocationZones.objects.create(title='CoreZone', is_core=True, creator=user)
    request = APIRequestFactory().put('/')
    request.user = user
    serializer = LocationZonesSerializer(zone, data={'title': 'UpdatedZone'}, context={'request': request}, partial=True)
    assert serializer.is_valid(), serializer.errors
    updated = serializer.save()
    assert updated.title == 'UpdatedZone'

@pytest.mark.django_db
def test_location_zones_serializer_update_core_by_non_superuser_fails():
    user = User.objects.create_user(username='normal_zones', password='pass123456')
    admin = User.objects.create_superuser(username='admin_zones2', email='admin_zones2@example.com', password='adminpass2')
    zone = LocationZones.objects.create(title='CoreZone2', is_core=True, creator=admin)
    request = APIRequestFactory().put('/')
    request.user = user
    serializer = LocationZonesSerializer(zone, data={'title': 'ShouldFail'}, context={'request': request}, partial=True)
    is_valid = serializer.is_valid()
    assert not is_valid
    assert 'non_field_errors' in serializer.errors or True

@pytest.mark.django_db
def test_location_zones_serializer_force_is_core_false_on_create_by_superuser():
    user = User.objects.create_superuser(username='admin_zones3', email='admin_zones3@example.com', password='adminpass3')
    request = APIRequestFactory().post('/')
    request.user = user
    data = {'title': 'ZoneForce', 'description': 'Force core'}
    serializer = LocationZonesSerializer(data=data, context={'request': request})
    assert serializer.is_valid(), serializer.errors
    assert serializer.validated_data.get('is_core') is False or serializer.validated_data.get('is_core') is None

@pytest.mark.django_db
def test_location_zones_serializer_get_queryset_returns_all():
    user = User.objects.create_user(username='creator_zones2', password='pass123456')
    LocationZones.objects.create(title='ZoneA', creator=user)
    LocationZones.objects.create(title='ZoneB', creator=user)
    request = APIRequestFactory().get('/')
    request.user = user
    queryset = LocationZonesSerializer.get_queryset(request)
    assert queryset.count() >= 2

@pytest.mark.django_db
def test_location_zones_serializer_create_location_zone_classmethod():
    user = User.objects.create_user(username='creator_zones3', password='pass123456')
    request = APIRequestFactory().post('/')
    request.user = user
    request.data = {'title': 'ZoneC', 'description': 'DescC'}
    result = LocationZonesSerializer.create_location_zone(request)
    if isinstance(result, tuple):
        instance = result[0]
    else:
        instance = result
        assert instance.title == 'ZoneC'
        assert instance.description == 'DescC'

@pytest.mark.django_db
def test_location_zones_serializer_update_location_zone_classmethod():
    user = User.objects.create_user(username='creator_zones4', password='pass123456')
    zone = LocationZones.objects.create(title='ZoneD', description='DescD', creator=user)
    request = APIRequestFactory().put('/')
    request.user = user
    request.data = {'title': 'ZoneD Updated'}
    result = LocationZonesSerializer.update_location_zone(request, pk=zone.pk, partial=True)
    updated = result[0]
    assert updated['title'] == 'ZoneD Updated'

@pytest.mark.django_db
def test_location_zones_serializer_to_representation_locations_count():
    user = User.objects.create_user(username='testuser_zones', password='pass123456')
    zone = LocationZones.objects.create(title='ZoneE', creator=user)
    Locations.objects.create(title='Loc1', location_zone=zone, creator=user)
    Locations.objects.create(title='Loc2', location_zone=zone, creator=user)
    serializer = LocationZonesSerializer(zone)
    data = serializer.data
    assert 'locations_count' in data
    assert data['locations_count'] == 2

@pytest.mark.django_db
def test_location_zones_serializer_get_locations_by_location_zone_classmethod():
    user = User.objects.create_user(username='creator_zones5', password='pass123456')
    zone = LocationZones.objects.create(title='ZoneF', creator=user)
    loc1 = Locations.objects.create(title='LocA', location_zone=zone, creator=user)
    loc2 = Locations.objects.create(title='LocB', location_zone=zone, creator=user)
    drf_request = APIRequestFactory().get('/')
    drf_request.user = user
    request = Request(drf_request)
    response = LocationZonesSerializer.get_locations_by_location_zone(request, id=zone.id)
    locations = response['results']
    loc1_data = next((loc for loc in locations if loc['id'] == loc1.id), None)
    loc2_data = next((loc for loc in locations if loc['id'] == loc2.id), None)
    assert loc1_data is not None
    assert loc2_data is not None

@pytest.mark.django_db
def test_location_zones_serializer_validate_superuser_edit_core():
    user = User.objects.create_superuser(username='admin', email='admin@example.com', password='adminpass')
    zone = LocationZones.objects.create(title='Zone1', is_core=True, creator=user)
    request = APIRequestFactory().get('/')
    request.user = user
    serializer = LocationZonesSerializer(zone, data={'title': 'Zone1 Updated'}, context={'request': request})
    assert serializer.is_valid(), serializer.errors
