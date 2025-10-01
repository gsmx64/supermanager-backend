import jwt
import pytest

from django.conf import settings
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User

from api.models import User


@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user(db):
    user = User.objects.create_user(username='testuser', password='testpass', email='test@example.com')
    return user

@pytest.fixture
def jwt_token(user):
    payload = {
        'user_id': user.id,
        'username': user.username,
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token if isinstance(token, str) else token.decode('utf-8')


"""
AppSettingsViewSet tests
"""
@pytest.mark.django_db
def test_app_settings_cache(api_client, user):
    api_client.force_authenticate(user=user)
    url = reverse('app-settings-list')
    response = api_client.get(url)
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT]
