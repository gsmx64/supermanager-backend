from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


class UserProfile(models.Model):
    """
    Model for user profile data.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    mobile = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    state = models.CharField(max_length=200, blank=True, null=True)
    zip_code = models.CharField(max_length=12, blank=True, null=True)
    country = models.CharField(max_length=200, blank=True, null=True)
    birth = models.DateField(blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    about = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    class Meta:
        managed = True
        db_table = 'api_userprofile'

@receiver(post_save, sender=User)
def create_profile_for_user(sender, instance, created, **kwargs):
    """
    Create a user profile when a new user is created.
    """
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile_for_user(sender, instance, **kwargs):
    """
    Save the user profile when the user is saved.
    """
    instance.profile.save()


class LocationZones(models.Model):
    """
    Model for location zone data.
    """
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    code_name = models.CharField(max_length=50, null=True, blank=True)
    status = models.PositiveIntegerField(null=False, blank=False, default=1)
    is_core = models.BooleanField(default=False)
    manager = models.CharField(max_length=200, blank=True)
    manager_email = models.CharField(max_length=200, blank=True)
    manager_phone = models.CharField(max_length=200, blank=True)
    manager_mobile = models.CharField(max_length=200, blank=True)
    sort_order = models.IntegerField(null=True, blank=True)
    creator = models.ForeignKey(User, unique=False, on_delete=models.CASCADE, related_name='location_zones_by_creator')
    updater = models.ForeignKey(User, unique=False, on_delete=models.CASCADE, null=True, blank=True, related_name='location_zones_by_updater')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        managed = True
        db_table = 'api_location_zones'


class Locations(models.Model):
    """
    Model for location data.
    """
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    code_name = models.CharField(max_length=50, null=True, blank=True)
    status = models.PositiveIntegerField(null=False, blank=False, default=1)
    is_core = models.BooleanField(default=False)
    location_zone = models.ForeignKey(LocationZones, on_delete=models.CASCADE, related_name='locations')
    manager = models.CharField(max_length=200, blank=True)
    manager_email = models.CharField(max_length=200, blank=True)
    manager_phone = models.CharField(max_length=200, blank=True)
    manager_mobile = models.CharField(max_length=200, blank=True)
    collaborator = models.CharField(max_length=200, blank=True)
    collaborator_email = models.CharField(max_length=200, blank=True)
    collaborator_phone = models.CharField(max_length=200, blank=True)
    collaborator_mobile = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=200, blank=True)
    mobile = models.CharField(max_length=200, blank=True)
    address = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=200, blank=True)
    zip_code = models.CharField(max_length=12, blank=True)
    country = models.CharField(max_length=200, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    sort_order = models.IntegerField(null=True, blank=True)
    creator = models.ForeignKey(User, unique=False, on_delete=models.CASCADE, related_name='locations_by_creator')
    updater = models.ForeignKey(User, unique=False, on_delete=models.CASCADE, null=True, blank=True, related_name='locations_by_updater')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        managed = True
        db_table = 'api_locations'


class DeviceTypes(models.Model):
    """
    Model for device types data.
    """
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    code_name = models.CharField(max_length=50, null=True, blank=True)
    status = models.PositiveIntegerField(null=False, blank=False, default=1)
    is_core = models.BooleanField(default=False)
    is_deprecated = models.BooleanField(default=False)
    sort_order = models.IntegerField(null=True, blank=True)
    creator = models.ForeignKey(User, unique=False, on_delete=models.CASCADE, related_name='device_types_by_creator')
    updater = models.ForeignKey(User, unique=False, on_delete=models.CASCADE, null=True, blank=True, related_name='device_types_by_updater')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        managed = True
        db_table = 'api_device_types'


class DeviceMarks(models.Model):
    """
    Model for device marks data.
    """
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    code_name = models.CharField(max_length=50, null=True, blank=True)
    status = models.PositiveIntegerField(null=False, blank=False, default=1)
    is_core = models.BooleanField(default=False)
    is_deprecated = models.BooleanField(default=False)
    sort_order = models.IntegerField(null=True, blank=True)
    creator = models.ForeignKey(User, unique=False, on_delete=models.CASCADE, related_name='device_marks_by_creator')
    updater = models.ForeignKey(User, unique=False, on_delete=models.CASCADE, null=True, blank=True, related_name='device_marks_by_updater')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        managed = True
        db_table = 'api_device_marks'


class DeviceModels(models.Model):
    """
    Model for device models data.
    """
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    code_name = models.CharField(max_length=50, null=True, blank=True)
    status = models.PositiveIntegerField(null=False, blank=False, default=1)
    is_core = models.BooleanField(default=False)
    is_deprecated = models.BooleanField(default=False)
    sort_order = models.IntegerField(null=True, blank=True)
    creator = models.ForeignKey(User, unique=False, on_delete=models.CASCADE, related_name='device_models_by_creator')
    updater = models.ForeignKey(User, unique=False, on_delete=models.CASCADE, null=True, blank=True, related_name='device_models_by_updater')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        managed = True
        db_table = 'api_device_models'


class DeviceSystems(models.Model):
    """
    Model for device systems data.
    """
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    code_name = models.CharField(max_length=50, null=True, blank=True)
    status = models.PositiveIntegerField(null=False, blank=False, default=1)
    is_core = models.BooleanField(default=False)
    is_deprecated = models.BooleanField(default=False)
    sort_order = models.IntegerField(null=True, blank=True)
    creator = models.ForeignKey(User, unique=False, on_delete=models.CASCADE, related_name='device_systems_by_creator')
    updater = models.ForeignKey(User, unique=False, on_delete=models.CASCADE, null=True, blank=True, related_name='device_systems_by_updater')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        managed = True
        db_table = 'api_device_systems'


class DeviceBuilds(models.Model):
    """
    Model for device builds data.
    """
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    code_name = models.CharField(max_length=50, null=True, blank=True)
    status = models.PositiveIntegerField(null=False, blank=False, default=1)
    is_core = models.BooleanField(default=False)
    is_deprecated = models.BooleanField(default=False)
    sort_order = models.IntegerField(null=True, blank=True)
    creator = models.ForeignKey(User, unique=False, on_delete=models.CASCADE, related_name='device_builds_by_creator')
    updater = models.ForeignKey(User, unique=False, on_delete=models.CASCADE, null=True, blank=True, related_name='device_builds_by_updater')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        managed = True
        db_table = 'api_device_builds'


class DeviceProcessors(models.Model):
    """
    Model for device processors data.
    """
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    code_name = models.CharField(max_length=50, null=True, blank=True)
    status = models.PositiveIntegerField(null=False, blank=False, default=1)
    is_core = models.BooleanField(default=False)
    is_deprecated = models.BooleanField(default=False)
    sort_order = models.IntegerField(null=True, blank=True)
    creator = models.ForeignKey(User, unique=False, on_delete=models.CASCADE, related_name='device_processors_by_creator')
    updater = models.ForeignKey(User, unique=False, on_delete=models.CASCADE, null=True, blank=True, related_name='device_processors_by_updater')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        managed = True
        db_table = 'api_device_processors'


class DeviceRAMs(models.Model):
    """
    Model for device RAMs data.
    """
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    code_name = models.CharField(max_length=50, null=True, blank=True)
    status = models.PositiveIntegerField(null=False, blank=False, default=1)
    is_core = models.BooleanField(default=False)
    is_deprecated = models.BooleanField(default=False)
    sort_order = models.IntegerField(null=True, blank=True)
    creator = models.ForeignKey(User, unique=False, on_delete=models.CASCADE, related_name='device_rams_by_creator')
    updater = models.ForeignKey(User, unique=False, on_delete=models.CASCADE, null=True, blank=True, related_name='device_rams_by_updater')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        managed = True
        db_table = 'api_device_rams'


class DeviceDisks(models.Model):
    """
    Model for device disks data.
    """
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    code_name = models.CharField(max_length=50, null=True, blank=True)
    status = models.PositiveIntegerField(null=False, blank=False, default=1)
    is_core = models.BooleanField(default=False)
    is_deprecated = models.BooleanField(default=False)
    sort_order = models.IntegerField(null=True, blank=True)
    creator = models.ForeignKey(User, unique=False, on_delete=models.CASCADE, related_name='device_disks_by_creator')
    updater = models.ForeignKey(User, unique=False, on_delete=models.CASCADE, null=True, blank=True, related_name='device_disks_by_updater')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        managed = True
        db_table = 'api_device_disks'


class Softwares(models.Model):
    """
    Model for software data.
    """
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    version = models.CharField(max_length=100, null=True, blank=True)
    code_name = models.CharField(max_length=50, null=True, blank=True)
    status = models.PositiveIntegerField(null=False, blank=False, default=1)
    is_core = models.BooleanField(default=False)
    is_deprecated = models.BooleanField(default=False)
    sort_order = models.IntegerField(null=True, blank=True)
    creator = models.ForeignKey(User, unique=False, on_delete=models.CASCADE, related_name='softwares_by_creator')
    updater = models.ForeignKey(User, unique=False, on_delete=models.CASCADE, null=True, blank=True, related_name='softwares_by_updater')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.version})"

    class Meta:
        managed = True
        db_table = 'api_softwares'


class Devices(models.Model):
    """
    Model for devices data.
    """
    id = models.AutoField(primary_key=True)
    internal_id = models.CharField(null=False, blank=False, max_length=200)
    status = models.PositiveIntegerField(null=False, blank=False, default=1)
    location = models.ForeignKey(Locations, on_delete=models.CASCADE, related_name='devices_location')
    type = models.ForeignKey(DeviceTypes, on_delete=models.CASCADE, related_name='devices_type')
    mark = models.ForeignKey(DeviceMarks, on_delete=models.CASCADE, related_name='devices_mark')
    model = models.ForeignKey(DeviceModels, on_delete=models.CASCADE, related_name='devices_model')
    hostname = models.CharField(null=True, blank=True, max_length=200)
    system = models.ForeignKey(DeviceSystems, on_delete=models.CASCADE, related_name='devices_system')
    build = models.ForeignKey(DeviceBuilds, on_delete=models.CASCADE, related_name='devices_build')
    processor = models.ForeignKey(DeviceProcessors, on_delete=models.CASCADE, related_name='devices_processor')
    ram = models.ForeignKey(DeviceRAMs, on_delete=models.CASCADE, related_name='devices_ram')
    disk = models.ForeignKey(DeviceDisks, on_delete=models.CASCADE, related_name='devices_disk')
    disk_internal_id = models.CharField(null=True, blank=True, max_length=200)
    disk_serial = models.CharField(null=True, blank=True, max_length=200)
    network_ipv4 = models.CharField(null=True, blank=True, max_length=200)
    network_ipv6 = models.CharField(null=True, blank=True, max_length=200)
    network_mac = models.CharField(null=True, blank=True, max_length=200)
    remote_id = models.CharField(null=True, blank=True, max_length=200)
    serial = models.CharField(null=True, blank=True, max_length=200)
    sector = models.CharField(null=True, blank=True, max_length=200)
    user_owner = models.CharField(null=True, blank=True, max_length=200)
    softwares = models.ManyToManyField(Softwares, through='DeviceSoftwares', related_name='devices_softwares')
    notes = models.TextField(null=True, blank=True)
    sort_order = models.IntegerField(null=True, blank=True)
    creator = models.ForeignKey(User, unique=False, on_delete=models.CASCADE, related_name='devices_by_creator')
    updater = models.ForeignKey(User, unique=False, on_delete=models.CASCADE, null=True, blank=True, related_name='devices_by_updater')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.internal_id} - {self.mark} {self.model} ({self.hostname})"

    class Meta:
        managed = True
        db_table = 'api_devices'


class DeviceSoftwares(models.Model):
    """
    Many-to-many relationship between Devices and Softwares.
    """
    id = models.AutoField(primary_key=True)
    device = models.ForeignKey(Devices, on_delete=models.CASCADE, related_name='device_softwares')
    software = models.ForeignKey(Softwares, on_delete=models.CASCADE, related_name='software_devices')
    installed_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        managed = True
        db_table = 'api_device_softwares'
        unique_together = ('device', 'software')


class NotificationTypes(models.Model):
    """
    Model for notification types data.
    """
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    status = models.PositiveIntegerField(null=False, blank=False, default=1)
    is_core = models.BooleanField(default=False)
    sort_order = models.IntegerField(null=True, blank=True)
    creator = models.ForeignKey(User, unique=False, on_delete=models.CASCADE, related_name='notification_types_by_creator')
    updater = models.ForeignKey(User, unique=False, on_delete=models.CASCADE, null=True, blank=True, related_name='notification_types_by_updater')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        managed = True
        db_table = 'api_notification_types'

   
class Notifications(models.Model):
    """
    Model for notifications data.
    """
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(null=True, blank=True)
    status = models.PositiveIntegerField(null=False, blank=False, default=1)
    type = models.ForeignKey(NotificationTypes, on_delete=models.CASCADE, related_name='notification_types', blank=True)
    module = models.CharField(max_length=200, blank=True)
    module_id = models.PositiveIntegerField(null=False, blank=True)
    sort_order = models.IntegerField(null=True, blank=True)
    creator = models.ForeignKey(User, unique=False, on_delete=models.CASCADE, related_name='notification_by_creator')
    updater = models.ForeignKey(User, unique=False, on_delete=models.CASCADE, null=True, blank=True, related_name='notification_by_updater')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        managed = True
        db_table = 'api_notifications'


class AppSettings(models.Model):
    """
    Singleton model for application-wide settings.
    """
    id = models.AutoField(primary_key=True)
    number_of_alerts = models.PositiveIntegerField(default=5)
    items_title_min_length = models.PositiveIntegerField(default=3)
    items_title_max_length = models.PositiveIntegerField(default=100)
    items_title_code_name_length = models.PositiveIntegerField(default=50)
    items_code_name_max_length = models.PositiveIntegerField(default=50)
    username_min_length = models.PositiveIntegerField(default=3)
    username_max_length = models.PositiveIntegerField(default=50)
    password_min_length = models.PositiveIntegerField(default=8)
    password_max_length = models.PositiveIntegerField(default=128)
    email_min_length = models.PositiveIntegerField(default=5)
    email_max_length = models.PositiveIntegerField(default=254)
    name_min_length = models.PositiveIntegerField(default=2)
    name_max_length = models.PositiveIntegerField(default=100)
    default_page_size = models.PositiveIntegerField(default=20)
    default_page_size_options = models.CharField(max_length=100, default="10,20,30,40,50,100")
    search_min_input_length = models.PositiveIntegerField(default=2)
    search_max_input_length = models.PositiveIntegerField(default=100)
    default_ordering_column = models.CharField(max_length=100, default="created_at")
    show_deprecated_only_in = models.CharField(max_length=100, default="models,systems,builds,processors,rams,disks,softwares")

    class Meta:
        managed = True
        db_table = 'api_app_settings'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class UserSettings(models.Model):
    """
    Singleton model for user-specific settings.
    """
    id = models.AutoField(primary_key=True)
    default_language = models.CharField(max_length=20, choices=[("en", "English"), ("es", "Spanish")], default="en")
    default_theme = models.CharField(max_length=20, choices=[("light", "Light"), ("dark", "Dark")], default="light")
    date_format_day = models.CharField(max_length=10, choices=[("numeric", "numeric"), ("2-digit", "2-digit")], default="2-digit")
    date_format_month = models.CharField(max_length=10, choices=[("numeric", "numeric"), ("2-digit", "2-digit")], default="2-digit")
    date_format_year = models.CharField(max_length=10, choices=[("numeric", "numeric"), ("2-digit", "2-digit")], default="numeric")
    timezone = models.CharField(max_length=50, default="America/New_York")
    time_24h = models.BooleanField(default=True)

    class Meta:
        managed = True
        db_table = 'api_user_settings'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
