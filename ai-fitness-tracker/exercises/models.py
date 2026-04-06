import uuid
from django.db import models


class Exercise(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=100)
    description = models.TextField()

    difficulty = models.CharField(max_length=50)
    muscle_group = models.CharField(max_length=100)

    calories_per_rep = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)