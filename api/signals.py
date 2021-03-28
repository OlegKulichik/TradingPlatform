from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework_simplejwt.state import User
from trading.models import Profile, WatchList


@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        WatchList.objects.create(profile=profile)