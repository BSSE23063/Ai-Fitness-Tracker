import uuid
from django.db import models
from django.conf import settings
from exercises.models import Exercise


User = settings.AUTH_USER_MODEL


class WorkoutSession(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="workout_sessions"
    )

    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)

    total_reps = models.IntegerField()
    total_calories = models.FloatField()

    duration_seconds = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    
    
    
class WorkoutExercise(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    session = models.ForeignKey(
        WorkoutSession,
        on_delete=models.CASCADE,
        related_name="exercises"
    )

    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.CASCADE
    )

    reps = models.IntegerField()
    sets = models.IntegerField()

    calories_burned = models.FloatField()
    duration_seconds = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)    