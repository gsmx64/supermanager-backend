import pytest

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.urls import reverse

from api.models import (
    Locations, LocationZones, DeviceTypes, DeviceMarks, DeviceModels,
    DeviceSystems, DeviceBuilds, DeviceProcessors, DeviceRAMs, DeviceDisks,
    Devices, NotificationTypes, Notifications, UserProfile
)
from api.admin import UserAdmin, UserProfileInline # Importa tus clases


# Obtener el modelo User de Django
User = get_user_model()

# Lista de modelos a verificar que están registrados
REGISTERED_MODELS = [
    User, UserProfile, Locations, LocationZones, DeviceTypes, DeviceMarks,
    DeviceModels, DeviceSystems, DeviceBuilds, DeviceProcessors, DeviceRAMs,
    DeviceDisks, Devices, NotificationTypes, Notifications
]


@pytest.mark.django_db
def test_all_models_registered_in_admin():
    """
    Verifica que todos los modelos de la lista estén registrados en el sitio de administración.
    """
    admin_site = admin.site
    for model in REGISTERED_MODELS:
        assert admin_site.is_registered(model), f"El modelo {model.__name__} no está registrado en el admin."


@pytest.mark.django_db
def test_user_admin_uses_custom_admin_class():
    """
    Verifica que el modelo User esté registrado con la clase UserAdmin.
    """
    admin_site = admin.site
    # Verifica que la clase registrada para User sea UserAdmin
    assert isinstance(admin_site._registry[User], UserAdmin)
    # Verifica que tenga la configuración de inlines esperada
    assert admin_site._registry[User].inlines == [UserProfileInline]


@pytest.mark.django_db
def test_user_admin_has_user_profile_inline_configured():
    """
    Verifica que UserProfileInline esté correctamente configurado.
    Como UserProfileInline es una subclase de StackedInline,
    podemos verificar su configuración.
    """
    # Se verifica la clase, no la instancia registrada.
    assert UserProfileInline.model == UserProfile
    assert UserProfileInline.can_delete == False
    assert issubclass(UserProfileInline, admin.StackedInline)


@pytest.mark.django_db
def test_custom_site_header_is_set():
    """
    Verifica que admin.site.site_header se haya personalizado.
    """
    assert admin.site.site_header == "SuperManager Admin"


@pytest.mark.django_db
def test_user_change_view_renders_userprofile_inline(admin_client, django_user_model):
    """
    Verifica que la vista de cambio de User (edición) muestre el inline de UserProfile.
    """
    # Creamos un usuario simple usando la fixture django_user_model
    user = django_user_model.objects.create_user(username='testuser', password='password123')
    
    # URL de la vista de cambio del usuario: /admin/auth/user/{user_id}/change/
    url = reverse('admin:auth_user_change', args=[user.pk])
    
    # Usamos admin_client, que está autenticado como superusuario
    response = admin_client.get(url)
    
    assert response.status_code == 200
    
    # ... el resto de la lógica de verificación ...
    inline_found = False
    for inline_formset in response.context['inline_admin_formsets']:
        # Importa UserProfileInline del módulo de admin
        from api.admin import UserProfileInline
        if isinstance(inline_formset.opts, UserProfileInline):
            inline_found = True
            break
            
    assert inline_found, "El inline UserProfileInline no se encontró en la vista de cambio de usuario."
