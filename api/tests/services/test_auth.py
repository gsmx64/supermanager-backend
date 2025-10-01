import pytest

from django.test import RequestFactory
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from api.services.auth import AuthService


@pytest.fixture
def factory():
    return RequestFactory()

@pytest.fixture
def user(db):
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123',
        first_name='Test',
        last_name='User',
        is_active=True
    )

@pytest.fixture
def admin(db):
    return User.objects.create_user(
        username='adminuser',
        email='admin@example.com',
        password='adminpass123',
        is_staff=True,
        is_active=True,
        is_superuser=True
    )

@pytest.mark.django_db
def test_validate_register_success():
    class DummySerializer:
        context = {'action': 'register'}
    data = {
        'username': 'newuser',
        'email': 'new@example.com',
        'password': 'pass123',
        'repeat_password': 'pass123',
        'first_name': 'New',
        'last_name': 'User'
    }
    result = AuthService.validate(DummySerializer, User, data)
    assert result['username'] == 'newuser'

def test_validate_register_password_mismatch():
    class DummySerializer:
        context = {'action': 'register'}
    data = {
        'username': 'newuser',
        'email': 'new@example.com',
        'password': 'pass123',
        'repeat_password': 'pass456',
        'first_name': 'New',
        'last_name': 'User'
    }
    with pytest.raises(serializers.ValidationError):
        AuthService.validate(DummySerializer, User, data)

def test_validate_login_success(user):
    class DummySerializer:
        context = {'action': 'login'}
    data = {
        'username': 'testuser',
        'password': 'testpass123'
    }
    result = AuthService.validate(DummySerializer, User, data)
    assert result['user'].username == 'testuser'

def test_validate_login_invalid_credentials(user):
    class DummySerializer:
        context = {'action': 'login'}
    data = {
        'username': 'testuser',
        'password': 'wrongpass'
    }
    with pytest.raises(AuthenticationFailed):
        AuthService.validate(DummySerializer, User, data)

def test_validate_change_password_wrong_current(factory, user):
    request = factory.post('/fake-url/', {'id': user.id})
    request.user = user
    class DummySerializer:
        context = {'action': 'change_password', 'request': request}
    data = {
        'id': user.id,
        'current_password': 'wrongpass',
        'password': 'newpass123',
        'repeat_password': 'newpass123'
    }
    result = AuthService.validate(DummySerializer, User, data)
    assert result['user'].password != data['current_password']

def test_validate_change_password_success_current(factory, user):
    request = factory.post('/fake-url/', {'id': user.id})
    request.user = user
    class DummySerializer:
        context = {'action': 'change_password', 'request': request}
    data = {
        'id': user.id,
        'current_password': 'testpass123',
        'password': 'newpass123',
        'repeat_password': 'newpass123'
    }
    result = AuthService.validate(DummySerializer, User, data)
    assert result['user'].username == 'testuser'

def test_validate_admin_change_password_not_admin(factory, user):
    request = factory.post('/fake-url/', {'id': user.id})
    request.user = user
    class DummySerializer:
        context = {'action': 'admin_change_password', 'request': request}
    data = {
        'id': user.id,
        'password': 'newpass123',
        'repeat_password': 'newpass123'
    }
    with pytest.raises(serializers.ValidationError):
        AuthService.validate(DummySerializer, User, data)

def test_validate_admin_change_password_success(factory, admin):
    request = factory.post('/fake-url/', {'id': admin.id})
    request.user = admin
    class DummySerializer:
        context = {'action': 'admin_change_password', 'request': request}
    data = {
        'id': admin.id,
        'password': 'newpass123',
        'repeat_password': 'newpass123'
    }
    result = AuthService.validate(DummySerializer, User, data)
    assert result['user'].username == 'adminuser'

@pytest.mark.django_db
def test_validate_forgot_password_email_not_found():
    class DummySerializer:
        context = {'action': 'forgot_password'}
    data = {'forgot_email': 'notfound@example.com'}
    result = AuthService.validate(DummySerializer, User, data)
    assert result is None

def test_validate_forgot_password_email_found(user):
    class DummySerializer:
        context = {'action': 'forgot_password'}
    data = {'forgot_email': 'test@example.com'}
    result = AuthService.validate(DummySerializer, User, data)
    assert result is data

def test_validate_access_token_success(user):
    class DummySerializer:
        context = {'action': 'access_token'}
    data = {
        'username': 'testuser',
        'password': 'testpass123'
    }
    result = AuthService.validate(DummySerializer, User, data)
    assert result['user'].username == 'testuser'

def test_validate_access_token_invalid(user):
    class DummySerializer:
        context = {'action': 'access_token'}
    data = {
        'username': 'testuser',
        'password': 'wrongpass'
    }
    with pytest.raises(serializers.ValidationError):
        AuthService.validate(DummySerializer, User, data)

def test_validate_refresh_token_missing():
    class DummySerializer:
        context = {'action': 'refresh_token'}
    data = {}
    with pytest.raises(serializers.ValidationError):
        AuthService.validate(DummySerializer, User, data)

def test_validate_refresh_token_success():
    class DummySerializer:
        context = {'action': 'refresh_token'}
    data = {'refresh': 'dummy_refresh_token'}
    result = AuthService.validate(DummySerializer, User, data)
    assert result['refresh'] == 'dummy_refresh_token'

def test_validate_verify_token_missing():
    class DummySerializer:
        context = {'action': 'verify_token'}
    data = {}
    with pytest.raises(AuthenticationFailed):
        AuthService.validate(DummySerializer, User, data)

def test_validate_verify_token_success():
    class DummySerializer:
        context = {'action': 'verify_token'}
    data = {'token': 'dummy_token'}
    result = AuthService.validate(DummySerializer, User, data)
    assert result['token'] == 'dummy_token'

def test_validate_invalid_action():
    class DummySerializer:
        context = {'action': 'invalid_action'}
    data = {}
    with pytest.raises(serializers.ValidationError):
        AuthService.validate(DummySerializer, User, data)
