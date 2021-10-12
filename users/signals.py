from django.db.models.signals import post_save
from .models import BaseUser
from django.dispatch import receiver
from .models import Profile


# When a User is saved, send post_save signal. receiver receives the signal. Decorator is using create_profile as a receiver

# REMEMBER TO IMPORT SIGNALS IN THE APP CONFIG'S READY METHOD

@receiver(post_save, sender=BaseUser)
def create_profile(sender, instance, created, **kwargs):
    """  Arguments come from post_save. If the user was created, creates a profile object linked to the user"""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=BaseUser)
def save_profile(sender, instance, **kwargs):
    """  Saves the profile created by calling create_profile"""
    instance.user_profile.save()
