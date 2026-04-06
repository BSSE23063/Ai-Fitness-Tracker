from django.contrib import admin
from .models import WorkoutExercise, WorkoutSession

admin.site.register(WorkoutSession)
admin.site.register(WorkoutExercise)