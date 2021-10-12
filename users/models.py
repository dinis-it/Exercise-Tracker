from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import settings
from PIL import Image
# Create your models here.


class BaseUser(AbstractUser):
    profile = models.OneToOneField(
        'Profile', on_delete=models.CASCADE, null=True, related_name="user_name")

    required = ['email']

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_profile')
    profile_picture = models.ImageField(
        default="default.png", upload_to="profile_pics")
    age = models.IntegerField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    # TODO one-to-many
    weight = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.user}'s Profile"


