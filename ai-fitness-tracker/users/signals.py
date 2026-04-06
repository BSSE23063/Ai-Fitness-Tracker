# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Profile

# @receiver is the event listener. 
# It listens for the 'post_save' event specifically from the 'User' model.
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    # 'instance' is the actual User object that was just saved.
    # 'created' is a boolean. True if a NEW user was created, False if an existing user was just updated.
    
    if created:
        # Since your Profile model requires these fields, we give them default starting values.
        Profile.objects.create(
            user=instance,
            age=0,
            height_cm=0.0,
            weight_kg=0.0,
            fitness_goal="Not set",
            experience_level="Not set"
        )