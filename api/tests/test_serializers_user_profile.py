import pytest

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from api.models import UserProfile
from api.serializers import UserProfileSerializer


"""
UserProfileSerializer tests
"""
@pytest.mark.django_db
def test_user_profile_serializer_fields():
    user = User.objects.create_user(username='profileuser', password='pass123456')
    user.profile.phone = '123456789'
    user.profile.mobile = '987654321'
    user.profile.address = 'Some Address'
    user.profile.city = 'Some City'
    user.profile.state = 'Some State'
    user.profile.zip_code = '54321'
    user.profile.country = 'Some Country'
    user.profile.birth = '1990-05-15'
    user.profile.title = 'Developer'
    user.profile.about = 'About profile'
    serializer = UserProfileSerializer(user.profile)
    data = serializer.data
    assert data['phone'] == '123456789'
    assert data['mobile'] == '987654321'
    assert data['address'] == 'Some Address'
    assert data['city'] == 'Some City'
    assert data['state'] == 'Some State'
    assert data['zip_code'] == '54321'
    assert data['country'] == 'Some Country'
    assert data['birth'] == '1990-05-15'
    assert data['title'] == 'Developer'
    assert data['about'] == 'About profile'
    assert 'avatar' in data

@pytest.mark.django_db
def test_user_profile_serializer_get_avatar_returns_url_if_avatar_exists(settings, tmpdir):
    # Configure MEDIA_ROOT and MEDIA_URL for the test
    media_root = tmpdir.mkdir("media")
    settings.MEDIA_ROOT = str(media_root)
    settings.MEDIA_URL = "/media/"
    user = User.objects.create_user(username='profileavatar', password='pass123456')
    avatar_file = SimpleUploadedFile("avatar2.jpg", b"file_content", content_type="image/jpeg")
    profile, created = UserProfile.objects.get_or_create(user=user)
    profile.avatar.save("avatar2.jpg", avatar_file, save=True)
    profile.refresh_from_db()
    user.refresh_from_db()
    serializer = UserProfileSerializer(profile)
    data = serializer.data
    assert data['avatar'] is not None
    assert data['avatar'].endswith('avatar2.jpg')

@pytest.mark.django_db
def test_user_profile_serializer_partial_update():
    user = User.objects.create_user(username='profileupdate', password='pass123456')
    user.profile.phone = '111'
    serializer = UserProfileSerializer(user.profile, data={'phone': '222'}, partial=True)
    assert serializer.is_valid(), serializer.errors
    updated_profile = serializer.save()
    assert updated_profile.phone == '222'

@pytest.mark.django_db
def test_user_profile_serializer_full_update():
    user = User.objects.create_user(username='profileupdate2', password='pass123456')
    user.profile.phone = '111'
    user.profile.city = 'Old City'
    user.profile.save()
    data = {
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
    serializer = UserProfileSerializer(user.profile, data=data)
    assert serializer.is_valid(), serializer.errors
    updated_profile = serializer.save()
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
def test_user_profile_serializer_avatar_none():
    user = User.objects.create_user(username='testuser2', password='pass123456')
    serializer = UserProfileSerializer(user.profile)
    assert serializer.data['avatar'] is None
