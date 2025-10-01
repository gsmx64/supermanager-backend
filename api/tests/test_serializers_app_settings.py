import pytest

from api.models import AppSettings
from api.serializers import AppSettingsSerializer


"""
AppSettingsSerializer tests
"""
@pytest.mark.django_db
def test_app_settings_serializer_fields():
    # Create an AppSettings instance
    app_settings = AppSettings.objects.create(
        number_of_alerts=5,
        items_title_min_length=3,
        items_title_max_length=100,
        items_title_code_name_length=50,
        items_code_name_max_length=50,
        username_min_length=3,
        username_max_length=50,
        password_min_length=8,
        password_max_length=128,
        email_min_length=5,
        email_max_length=254,
        name_min_length=2,
        name_max_length=100,
        default_page_size=20,
        default_page_size_options='10,20,50,100',
        search_min_input_length=2,
        search_max_input_length=100,
        default_ordering_column='created_at',
        show_deprecated_only_in='models,systems,builds,processors,rams,disks,softwares'
    )
    serializer = AppSettingsSerializer(app_settings)
    data = serializer.data
    assert 'number_of_alerts' in data
    assert data['number_of_alerts'] == 5

    assert 'items_title_min_length' in data
    assert data['items_title_min_length'] == 3

    assert 'items_title_max_length' in data
    assert data['items_title_max_length'] == 100

    assert 'items_title_code_name_length' in data
    assert data['items_title_code_name_length'] == 50

    assert 'items_code_name_max_length' in data
    assert data['items_code_name_max_length'] == 50

    assert 'username_min_length' in data
    assert data['username_min_length'] == 3

    assert 'username_max_length' in data
    assert data['username_max_length'] == 50

    assert 'password_min_length' in data
    assert data['password_min_length'] == 8

    assert 'password_max_length' in data
    assert data['password_max_length'] == 128

    assert 'email_min_length' in data
    assert data['email_min_length'] == 5

    assert 'email_max_length' in data
    assert data['email_max_length'] == 254

    assert 'name_min_length' in data
    assert data['name_min_length'] == 2

    assert 'name_max_length' in data
    assert data['name_max_length'] == 100

    assert 'default_page_size' in data
    assert data['default_page_size'] == 20

    assert 'default_page_size_options' in data
    assert data['default_page_size_options'] == '10,20,50,100'

    assert 'search_min_input_length' in data
    assert data['search_min_input_length'] == 2

    assert 'search_max_input_length' in data
    assert data['search_max_input_length'] == 100

    assert 'default_ordering_column' in data
    assert data['default_ordering_column'] == 'created_at'

    assert 'show_deprecated_only_in' in data
    assert data['show_deprecated_only_in'] == 'models,systems,builds,processors,rams,disks,softwares'
