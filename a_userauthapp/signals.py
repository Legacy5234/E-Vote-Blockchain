from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from .models import Voter_User, Profile

# Create or update profile when a new user is created or updated
@receiver(post_save, sender=Voter_User)
def create_or_update_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, email=instance.email)
    else:
        profile, _ = Profile.objects.get_or_create(user=instance)
        if profile.email != instance.email:
            profile.email = instance.email
            profile.save(update_fields=['email'])

# Only update the user's email if the profile email changes — avoid recursion
@receiver(post_save, sender=Profile)
def sync_profile_to_user(sender, instance, created, **kwargs):
    if not created:
        user = instance.user
        if user.email != instance.email:
            Voter_User.objects.filter(id=user.id).update(email=instance.email)
