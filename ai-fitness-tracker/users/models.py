# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # AbstractUser automatically includes username, email, password, etc.

class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    
    age = models.IntegerField()
    height_cm = models.FloatField()
    weight_kg = models.FloatField()
    fitness_goal = models.CharField(max_length=100)
    experience_level = models.CharField(max_length=100)