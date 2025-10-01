import pytest

from django.contrib.auth.models import User

from api.models import UserSettings
from api.serializers import UserSettingsSerializer


"""
UserSettingsSerializer tests
"""
@pytest.mark.django_db
def test_user_settings_serializer_fields():
    # Create an UserSettings instance
    user = User.objects.create_user(username='testuser5', password='pass123456')
    user_settings = UserSettings.objects.create(
        id=user, 
        default_language='en',
        default_theme='light',
        date_format_day='2-digit',
        date_format_month='2-digit',
        date_format_year='numeric',
        timezone='America/New_York',
        time_24h=True
    )
    serializer = UserSettingsSerializer(user_settings)
    data = serializer.data
    assert 'default_language' in data
    assert data['default_language'] == 'en'
    
    assert 'default_theme' in data
    assert data['default_theme'] == 'light'
    
    assert 'date_format_day' in data
    assert data['date_format_day'] == '2-digit'
    
    assert 'date_format_month' in data
    assert data['date_format_month'] == '2-digit'
    
    assert 'date_format_year' in data
    assert data['date_format_year'] == 'numeric'
    
    assert 'timezone' in data
    assert data['timezone'] == 'America/New_York'
    
    assert 'time_24h' in data
    assert data['time_24h'] is True
