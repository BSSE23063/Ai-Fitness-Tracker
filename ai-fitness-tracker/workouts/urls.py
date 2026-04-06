from django.urls import path
from .views import start_workout, save_exercise, workout_history

urlpatterns = [

    path("start/", start_workout),

    path("save-exercise/", save_exercise),

    path("history/", workout_history),
]