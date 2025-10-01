import pytest

from rest_framework import routers
from api import urls


def test_router_instance():
    assert isinstance(urls.router, routers.DefaultRouter)

def test_urlpatterns_is_list():
    assert isinstance(urls.urlpatterns, list)

@pytest.mark.parametrize("route", [
    'auth', 'users', 'profile', 'locations', 'location-zones',
    'device-types', 'device-marks', 'device-models', 'device-systems',
    'device-builds', 'device-processors', 'device-rams', 'device-disks',
    'softwares', 'devices', 'device-softwares', 'notification-types',
    'notifications', 'app-settings', 'user-settings'
])
def test_router_has_registered_routes(route):
    registered_routes = [prefix for prefix, _, _ in urls.router.registry]
    assert route in registered_routes
