from rest_framework import serializers
from .models import WorkoutSession, WorkoutExercise


class WorkoutExerciseSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkoutExercise
        fields = "__all__"


class WorkoutSessionSerializer(serializers.ModelSerializer):

    exercises = WorkoutExerciseSerializer(many=True, read_only=True)

    class Meta:
        model = WorkoutSession
        fields = "__all__"