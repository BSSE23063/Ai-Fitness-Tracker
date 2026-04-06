from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated # Changed to IsAuthenticated
from django.utils import timezone

from exercises.models import Exercise
from .models import WorkoutSession, WorkoutExercise
from .serializers import WorkoutSessionSerializer, WorkoutExerciseSerializer

# =========================
# START WORKOUT SESSION
# =========================
@api_view(['POST'])
@permission_classes([IsAuthenticated]) # Requires JWT token!
def start_workout(request):
    # The JWT token already knows who the user is! No need to grab it from request.data
    user = request.user 

    session = WorkoutSession.objects.create(
        user=user,
        start_time=timezone.now(),
        end_time=timezone.now(),  # temporary fix is perfect here
        total_reps=0,
        total_calories=0,
        duration_seconds=0
    )

    return Response(WorkoutSessionSerializer(session).data, status=201)


# =========================
# SAVE EXERCISE RESULT
# =========================
@api_view(['POST'])
@permission_classes([IsAuthenticated]) # Requires JWT token!
def save_exercise(request):
    session_id = request.data.get("session_id")
    exercise_id = request.data.get("exercise_id")
    reps = request.data.get("reps")
    sets = request.data.get("sets", 1) # Defaults to 1 if not provided

    if not all([session_id, exercise_id, reps]):
        return Response({"error": "Missing session_id, exercise_id, or reps"}, status=400)

    try:
        # We also check that the session actually belongs to the logged-in user!
        session = WorkoutSession.objects.get(id=session_id, user=request.user)
    except WorkoutSession.DoesNotExist:
        return Response({"error": "Invalid session or not your session"}, status=404)

    try:
        exercise = Exercise.objects.get(id=exercise_id)
    except Exercise.DoesNotExist:
        return Response({"error": "Invalid exercise"}, status=404)

    calories = int(reps) * exercise.calories_per_rep

    workout = WorkoutExercise.objects.create(
        session=session,
        exercise=exercise,
        reps=reps,
        sets=sets,
        calories_burned=calories,
        duration_seconds=0
    )

    return Response(WorkoutExerciseSerializer(workout).data, status=201)


# =========================
# HISTORY
# =========================
@api_view(['GET'])
@permission_classes([IsAuthenticated]) # Requires JWT token!
def workout_history(request):
    # Grab ONLY the sessions for the currently logged-in user
    sessions = WorkoutSession.objects.filter(user=request.user).order_by('-start_time')

    return Response(WorkoutSessionSerializer(sessions, many=True).data)