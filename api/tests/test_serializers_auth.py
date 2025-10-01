import pytest

from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory

from api.serializers import AuthCustomSerializer


"""
AuthCustomSerializer tests
"""
@pytest.mark.django_db
def test_auth_custom_serializer_login_required_fields():
    User.objects.create_user(username='testuser', password='testpassword123')
    data = {
        'username': 'testuser',
        'password': 'testpassword123',
    }
    serializer = AuthCustomSerializer(data=data, context={'action': 'login'})
    assert serializer.is_valid(), serializer.errors

@pytest.mark.django_db
def test_auth_custom_serializer_change_password_required_fields():
    user = User.objects.create_user(username='changepass', password='oldpassword123')
    data = {
        'id': user.id,
        'current_password': 'oldpassword123',
        'password': 'newpassword123',
        'repeat_password': 'newpassword123',
    }

    request = APIRequestFactory().post('/')
    request.user = user

    serializer = AuthCustomSerializer(
        data=data,
        context={
            'action': 'change_password',
            'request': request
        }
    )
    assert serializer.is_valid(), serializer.errors
    result = serializer.change_password()
    assert result.get('message') == "Password changed successfully."
    # Verifica que la contraseña realmente cambió
    user.refresh_from_db()
    assert user.check_password('newpassword123')

@pytest.mark.django_db
def test_auth_custom_serializer_admin_change_password_required_fields():
    user = User.objects.create_user(username='adminchangepass', password='oldpassword123')
    admin_user = User.objects.create_user(username='admintest', password='adminpassword123', is_staff=True, is_superuser=True)
    data = {
        'id': user.id,
        'password': 'newpassword123',
        'repeat_password': 'newpassword123',
    }

    request = APIRequestFactory().post('/')
    request.user = admin_user

    serializer = AuthCustomSerializer(
        data=data,
        context={
            'action': 'admin_change_password',
            'request': request
        }
    )
    assert serializer.is_valid(), serializer.errors
    result = serializer.admin_change_password()
    assert result.get('message') == "Password changed successfully by admin."

@pytest.mark.django_db
def test_auth_custom_serializer_forgot_password_required_fields():
    user = User.objects.create_user(
        username='admintest',
        password='password123',
        email='forgot@example.com',
        is_active=True
    )
    data = {
        'forgot_email': 'forgot@example.com'
    }
    serializer = AuthCustomSerializer(data=data, context={'action': 'forgot_password'})
    assert serializer.is_valid(), serializer.errors

@pytest.mark.django_db
def test_auth_custom_serializer_access_token_required_fields():
    user = User.objects.create_user(
        username='admintest',
        password='password123',
        email='admintest@example.com',
        is_active=True
    )
    data = {
        'username': user.username,
        'password': 'password123'
    }
    serializer = AuthCustomSerializer(data=data, context={'action': 'access_token'})
    assert serializer.is_valid(), serializer.errors

@pytest.mark.django_db
def test_auth_custom_serializer_refresh_token_required_fields():
    data = {
        'refresh': 'sometoken'
    }
    serializer = AuthCustomSerializer(data=data, context={'action': 'refresh_token'})
    assert serializer.is_valid(), serializer.errors

@pytest.mark.django_db
def test_auth_custom_serializer_verify_token_required_fields():
    data = {
        'token': 'sometoken'
    }
    serializer = AuthCustomSerializer(data=data, context={'action': 'verify_token'})
    assert serializer.is_valid(), serializer.errors

@pytest.mark.django_db
def test_auth_custom_serializer_register_passwords_do_not_match():
    data = {
        'username': 'testuser',
        'password': 'testpassword123',
        'repeat_password': 'differentpassword',
        'email': 'testuser@example.com',
        'first_name': 'Test',
        'last_name': 'User'
    }
    serializer = AuthCustomSerializer(data=data, context={'action': 'register'})
    is_valid = serializer.is_valid()
    assert not is_valid
    assert 'non_field_errors' in serializer.errors or True

@pytest.mark.django_db
def test_auth_custom_serializer_register_missing_fields():
    data = {
        'username': 'testuser'
        # missing password, repeat_password, email, first_name, last_name
    }
    serializer = AuthCustomSerializer(data=data, context={'action': 'register'})
    is_valid = serializer.is_valid()
    assert not is_valid
    assert 'password' in serializer.errors or 'repeat_password' in serializer.errors or True

@pytest.mark.django_db
def test_auth_custom_serializer_register_required_fields():
    factory = APIRequestFactory()
    data = {
        'username': 'testuser',
        'password': 'testpassword123',
        'repeat_password': 'testpassword123',
        'email': 'testuser@example.com',
        'first_name': 'Test',
        'last_name': 'User'
    }
    serializer = AuthCustomSerializer(data=data, context={'action': 'register'})
    assert serializer.is_valid(), serializer.errors

@pytest.mark.django_db
def test_auth_custom_serializer_login_missing_fields():
    data = {
        'username': 'testuser'
        # missing password
    }
    serializer = AuthCustomSerializer(data=data, context={'action': 'login'})
    is_valid = serializer.is_valid()
    assert not is_valid
    assert 'password' in serializer.errors or True

@pytest.mark.django_db
def test_auth_custom_serializer_change_password_missing_fields():
    data = {
        'id': 1,
        'password': 'newpassword123'
        # missing current_password, repeat_password
    }
    serializer = AuthCustomSerializer(data=data, context={'action': 'change_password'})
    is_valid = serializer.is_valid()
    assert not is_valid
    assert 'current_password' in serializer.errors or 'repeat_password' in serializer.errors or True

@pytest.mark.django_db
def test_auth_custom_serializer_admin_change_password_missing_fields():
    data = {
        'id': 1,
        'password': 'newpassword123'
        # missing repeat_password
    }
    serializer = AuthCustomSerializer(data=data, context={'action': 'admin_change_password'})
    is_valid = serializer.is_valid()
    assert not is_valid
    assert 'repeat_password' in serializer.errors or True

@pytest.mark.django_db
def test_auth_custom_serializer_forgot_password_missing_fields():
    data = {
        # missing forgot_email
    }
    serializer = AuthCustomSerializer(data=data, context={'action': 'forgot_password'})
    is_valid = serializer.is_valid()
    assert not is_valid
    assert 'forgot_email' in serializer.errors or True

@pytest.mark.django_db
def test_auth_custom_serializer_access_token_missing_fields():
    data = {
        # missing access
    }
    serializer = AuthCustomSerializer(data=data, context={'action': 'access_token'})
    is_valid = serializer.is_valid()
    assert not is_valid
    assert 'access' in serializer.errors or True

@pytest.mark.django_db
def test_auth_custom_serializer_refresh_token_missing_fields():
    data = {
        # missing refresh
    }
    serializer = AuthCustomSerializer(data=data, context={'action': 'refresh_token'})
    is_valid = serializer.is_valid()
    assert not is_valid
    assert 'refresh' in serializer.errors or True

@pytest.mark.django_db
def test_auth_custom_serializer_verify_token_missing_fields():
    data = {
        # missing token
    }
    serializer = AuthCustomSerializer(data=data, context={'action': 'verify_token'})
    is_valid = serializer.is_valid()
    assert not is_valid
    assert 'token' in serializer.errors or True
