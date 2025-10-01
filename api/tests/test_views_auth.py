import pytest

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
def admin_user(db):
    user = User.objects.create_superuser(username='admin', password='adminpass', email='admin@example.com')
    return user

"""
AuthCustomViewSet tests
"""
import json

@pytest.mark.django_db
def test_auth_register(api_client):
    url = reverse('auth-register')
    data = {
        "username": "newuser",
        "password": "newpass123",
        "repeat_password": "newpass123",
        "email": "newuser@example.com",
        "first_name": "New_",
        "last_name": "User"
    }
    response = api_client.post(url, data=json.dumps(data), content_type="application/json")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["username"] == "newuser"

@pytest.mark.django_db
def test_auth_login(api_client, user):
    url = reverse('auth-login')
    data = {
        "username": user.username,
        "password": "testpass"
    }
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data

@pytest.mark.django_db
def test_auth_change_password(api_client, user):
    api_client.force_authenticate(user=user)
    url = reverse('auth-change-password')
    data = {
        "id": user.id,
        "current_password": "testpass",
        "password": "newpass123",
        "repeat_password": "newpass123"
    }
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_auth_admin_change_password(api_client, admin_user, user):
    api_client.force_authenticate(user=admin_user)
    url = reverse('auth-admin-change-password')
    data = {
        "id": user.id,
        "password": "adminchangedpass",
        "repeat_password": "adminchangedpass"
    }
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_auth_forgot_password(api_client, user):
    url = reverse('auth-forgot-password')
    data = {
        "forgot_email": user.email
    }
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_auth_access_token(api_client, user):
    url = reverse('auth-access-token')
    data = {
        "username": user.username,
        "password": "testpass"
    }
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data

@pytest.mark.django_db
def test_auth_refresh_token(api_client, user):
    # First, get a token
    url_login = reverse('auth-login')
    data_login = {
        "username": user.username,
        "password": "testpass"
    }
    response_login = api_client.post(url_login, data_login)
    refresh_token = response_login.data.get("refresh")
    url_refresh = reverse('auth-refresh-token')
    data_refresh = {"refresh": refresh_token}
    response = api_client.post(url_refresh, data_refresh)
    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data

@pytest.mark.django_db
def test_auth_verify_token(api_client, user):
    url_login = reverse('auth-login')
    data_login = {
        "username": user.username,
        "password": "testpass"
    }
    response_login = api_client.post(url_login, data_login)
    access_token = response_login.data.get("access")
    url_verify = reverse('auth-verify-token')
    data_verify = {"token": access_token}
    response = api_client.post(url_verify, data_verify)
    assert response.status_code == status.HTTP_200_OK
