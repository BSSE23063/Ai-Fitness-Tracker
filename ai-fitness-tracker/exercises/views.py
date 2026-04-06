from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Exercise
from .serializers import ExerciseSerializer

@api_view(['GET', 'POST'])
def list_exercises(request):
    
    # If Postman sends a GET request, return all the exercises
    if request.method == 'GET':
        exercises = Exercise.objects.all()
        serializer = ExerciseSerializer(exercises, many=True)
        return Response(serializer.data)
        
    # If Postman sends a POST request, save the new exercise to the database
    elif request.method == 'POST':
        serializer = ExerciseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # If the data is missing something required, tell Postman what went wrong
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)