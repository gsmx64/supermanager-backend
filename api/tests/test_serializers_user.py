import pytest

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from api.serializers import UserSerializer


"""
UserSerializer tests
"""
@pytest.mark.django_db
def test_user_serializer_fields():
    user = User.objects.create_user(
        username='fieldsuser', email='fields@example.com',
        first_name='Fields', last_name='User', password='pass123456'
    )
    serializer = UserSerializer(user)
    data = serializer.data
    assert set(data.keys()) == {
        'id', 'username', 'email', 'first_name', 'last_name',
        'is_active', 'is_staff', 'is_superuser', 'date_joined', 'last_login', 'avatar'
    }
    assert data['username'] == 'fieldsuser'
    assert data['email'] == 'fields@example.com'
    assert data['first_name'] == 'Fields'
    assert data['last_name'] == 'User'
    assert data['is_active'] is True
    assert data['is_staff'] is False
    assert data['is_superuser'] is False

@pytest.mark.django_db
def test_user_serializer_avatar_none_when_no_profile():
    user = User.objects.create_user(username='noprof', password='pass123456')
    serializer = UserSerializer(user)
    data = serializer.data
    assert 'avatar' in data
    assert data['avatar'] is None

@pytest.mark.django_db
def test_user_serializer_avatar_url_when_profile_avatar_exists(settings, tmpdir):
    user = User.objects.create_user(username='avataruser3', password='pass123456')
    avatar_file = SimpleUploadedFile("avatar3.jpg", b"file_content", content_type="image/jpeg")
    user.profile.avatar = avatar_file
    user.profile.save()
    serializer = UserSerializer(user)
    data = serializer.data
    assert data['avatar'] is not None
    assert data['avatar'].startswith('/media/avatars/avatar3') and data['avatar'].endswith('.jpg')

@pytest.mark.django_db
def test_user_serializer_last_login_and_date_joined_are_serialized():
    user = User.objects.create_user(username='datetimes', password='pass123456')
    serializer = UserSerializer(user)
    data = serializer.data
    assert 'date_joined' in data
    assert data['date_joined'] is not None
    assert 'last_login' in data

@pytest.mark.django_db
def test_user_serializer_handles_missing_profile_gracefully():
    user = User.objects.create_user(username='missingprofile', password='pass123456')
    serializer = UserSerializer(user)
    data = serializer.data
    assert data['avatar'] is None

@pytest.mark.django_db
def test_user_serializer_is_staff_and_is_superuser_flags():
    user = User.objects.create_superuser(username='superuser', email='super@example.com', password='pass123456')
    serializer = UserSerializer(user)
    data = serializer.data
    assert data['is_staff'] is True
    assert data['is_superuser'] is True

@pytest.mark.django_db
def test_user_serializer_representation():
    user = User.objects.create_user(
        username='testuser', email='test@example.com',
        first_name='Test', last_name='User', password='pass123456'
    )
    serializer = UserSerializer(user)
    data = serializer.data
    assert data['username'] == 'testuser'
    assert data['email'] == 'test@example.com'
    assert 'avatar' in data
