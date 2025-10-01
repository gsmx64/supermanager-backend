import pytest

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from api.models import UserProfile
from api.serializers import UserExtendedSerializer


"""
UserExtendedSerializer tests
"""
@pytest.mark.django_db
def test_user_extended_serializer_fields_and_representation():
    user = User.objects.create_user(
        username='extendeduser', email='extended@example.com',
        first_name='Extended', last_name='User', password='pass123456'
    )
    user.profile.phone = '123456789'
    user.profile.mobile = '987654321'
    user.profile.address = '123 Main St'
    user.profile.city = 'Test City'
    user.profile.state = 'Test State'
    user.profile.zip_code = '12345'
    user.profile.country = 'Test Country'
    user.profile.birth = '2000-01-01'
    user.profile.title = 'Engineer'
    user.profile.about = 'About user'
    user.profile.save()
    serializer = UserExtendedSerializer(user)
    data = serializer.data
    assert data['username'] == 'extendeduser'
    assert data['email'] == 'extended@example.com'
    assert data['first_name'] == 'Extended'
    assert data['last_name'] == 'User'

@pytest.mark.django_db
def test_user_extended_serializer_missing_profile_fields():
    user = User.objects.create_user(
        username='noprof', email='noprof@example.com',
        first_name='No', last_name='Profile', password='pass123456'
    )
    # No UserProfile created
    serializer = UserExtendedSerializer(user)
    data = serializer.data
    assert data['phone'] == ''
    assert data['mobile'] == ''
    assert data['address'] == ''
    assert data['city'] == ''
    assert data['state'] == ''
    assert data['zip_code'] == ''
    assert data['country'] == ''
    assert data['birth'] == ''
    assert data['title'] == ''
    assert data['about'] == ''
    assert data['avatar'] == ''

@pytest.mark.django_db
def test_user_extended_serializer_partial_update_only_profile_fields():
    user = User.objects.create_user(username='partialuser', email='partial@example.com', password='pass123456')
    user.profile.phone = '111'
    user.profile.address = 'Old Address'
    user.profile.save()
    data = {
        'phone': '222',
        'address': 'Partial Address'
    }
    serializer = UserExtendedSerializer(user, data=data, partial=True)
    assert serializer.is_valid(), serializer.errors
    updated_user = serializer.save()
    updated_profile = updated_user.profile
    assert updated_profile.phone == '222'
    assert updated_profile.address == 'Partial Address'

@pytest.mark.django_db
def test_user_extended_serializer_representation_includes_all_fields():
    user = User.objects.create_user(
        username='fulluser', email='full@example.com',
        first_name='Full', last_name='User', password='pass123456',
        is_active=True, is_staff=True, is_superuser=True
    )
    profile, _ = UserProfile.objects.get_or_create(
        user=user, defaults={
            'phone': '555', 'mobile': '666', 'address': 'Full Address',
            'city': 'Full City', 'state': 'Full State', 'zip_code': '99999',
            'country': 'Full Country', 'birth': '1980-05-05', 'title': 'FullTitle', 'about': 'Full about'
        }
    )
    serializer = UserExtendedSerializer(user)
    data = serializer.data
    for field in [
        'id', 'username', 'email', 'first_name', 'last_name', 'is_active',
        'is_staff', 'is_superuser', 'date_joined', 'last_login',
        'avatar', 'title', 'phone', 'mobile', 'address', 'city', 'state',
        'zip_code', 'country', 'birth', 'about'
    ]:
        assert field in data

@pytest.mark.django_db
def test_user_extended_serializer_blank_profile_fields():
    user = User.objects.create_user(username='blankuser', email='blank@example.com', password='pass123456')
    user.profile.phone = ''
    user.profile.mobile = ''
    user.profile.address = ''
    user.profile.city = ''
    user.profile.state = ''
    user.profile.zip_code = ''
    user.profile.country = ''
    user.profile.birth = None
    user.profile.title = ''
    user.profile.about = ''
    user.profile.save()
    serializer = UserExtendedSerializer(user)
    data = serializer.data
    assert data['phone'] == ''
    assert data['mobile'] == ''
    assert data['address'] == ''
    assert data['city'] == ''
    assert data['state'] == ''
    assert data['zip_code'] == ''
    assert data['country'] == ''
    assert data['birth'] == ''
    assert data['title'] == ''
    assert data['about'] == ''

@pytest.mark.django_db
def test_user_extended_serializer_validate_username_unique():
    user1 = User.objects.create_user(username='uniqueuser', email='unique1@example.com', password='pass123456')
    user2 = User.objects.create_user(username='otheruser', email='unique2@example.com', password='pass123456')
    serializer = UserExtendedSerializer(user2, data={'username': 'uniqueuser'}, partial=True)
    is_valid = serializer.is_valid()
    assert not is_valid
    assert 'username' in serializer.errors

@pytest.mark.django_db
def test_user_extended_serializer_validate_email_unique():
    user1 = User.objects.create_user(username='usera', email='uniqueemail@example.com', password='pass123456')
    user2 = User.objects.create_user(username='userb', email='otheremail@example.com', password='pass123456')
    serializer = UserExtendedSerializer(user2, data={'email': 'uniqueemail@example.com'}, partial=True)
    is_valid = serializer.is_valid()
    assert not is_valid
    assert 'email' in serializer.errors

@pytest.mark.django_db
def test_user_extended_serializer_update_profile_fields():
    user = User.objects.create_user(username='updateuser', email='update@example.com', password='pass123456')
    user.profile.phone = '111'
    user.profile.mobile = '222'
    user.profile.save()
    data = {
        'username': 'updateuser',
        'phone': '333',
        'mobile': '444',
        'address': 'New Address',
        'city': 'New City',
        'state': 'New State',
        'zip_code': '54321',
        'country': 'New Country',
        'birth': '1999-12-31',
        'title': 'Manager',
        'about': 'Updated about'
    }
    serializer = UserExtendedSerializer(user, data=data)
    assert serializer.is_valid(), serializer.errors
    updated_user = serializer.save()
    updated_profile = updated_user.profile
    assert updated_profile.phone == '333'
    assert updated_profile.mobile == '444'
    assert updated_profile.address == 'New Address'
    assert updated_profile.city == 'New City'
    assert updated_profile.state == 'New State'
    assert updated_profile.zip_code == '54321'
    assert updated_profile.country == 'New Country'
    assert str(updated_profile.birth) == '1999-12-31'
    assert updated_profile.title == 'Manager'
    assert updated_profile.about == 'Updated about'

@pytest.mark.django_db
def test_user_extended_serializer_get_avatar_returns_empty_if_no_avatar():
    user = User.objects.create_user(username='avataruser', password='pass123456')
    serializer = UserExtendedSerializer(user)
    data = serializer.data
    assert data['avatar'] == ''

@pytest.mark.django_db
def test_user_extended_serializer_get_avatar_returns_url_if_avatar_exists(settings, tmpdir):
    # Configure MEDIA_ROOT and MEDIA_URL for the test
    media_root = tmpdir.mkdir("media")
    settings.MEDIA_ROOT = str(media_root)
    settings.MEDIA_URL = "/media/"
    user = User.objects.create_user(username='avataruser', password='pass123456')
    avatar_file = SimpleUploadedFile("avatar.jpg", b"file_content", content_type="image/jpeg")
    profile, created = UserProfile.objects.get_or_create(user=user)
    profile.avatar.save("avatar.jpg", avatar_file, save=True)
    profile.refresh_from_db()
    user.refresh_from_db()
    serializer = UserExtendedSerializer(user)
    data = serializer.data
    assert data['avatar'] is not None
    assert data['avatar'].endswith('avatar.jpg')

@pytest.mark.django_db
def test_user_extended_serializer_update():
    user = User.objects.create_user(username='testuser3', email='test3@example.com', password='pass123456')
    user.profile.phone = '123456789'
    user.profile.save()
    data = {
        'username': 'testuser3',
        'phone': '987654321'
    }
    serializer = UserExtendedSerializer(user, data=data)
    assert serializer.is_valid(), serializer.errors
    updated_user = serializer.save()
    assert updated_user.profile.phone == '987654321'
