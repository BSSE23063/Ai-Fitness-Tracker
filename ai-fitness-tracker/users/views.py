# views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework import status

from rest_framework.permissions import AllowAny

from .serializers import UserSerializer

from .serializers import ProfileSerializer

from django.contrib.auth.hashers import check_password

@api_view(["GET"])
@permission_classes([IsAuthenticated]) # This is your middleware!
def current_user(request):
    # Because of the middleware, request.user is already authenticated and fetched
    user = request.user
    return Response({
        "id": str(user.id),
        "username": user.username,
        "email": user.email
    })
    
    
    
    
@api_view(['POST'])
@permission_classes([AllowAny]) # Anyone can hit this route!
def register_user(request):
    # 1. Pass the incoming JSON data to our Serializer (like req.body)
    serializer = UserSerializer(data=request.data)

    # 2. Automatically validate the data 
    # (Checks if email is valid, username is unique, etc.)
    if serializer.is_valid():
        
        # 3. Save the user to the database 
        # (This triggers the `.create()` method in our serializer, securely hashing the password)
        user = serializer.save()

        # 4. Return a success response (Status 201: Created)
        return Response({
            "message": "User registered successfully!",
            "user": {
                "id": str(user.id),
                "username": user.username,
                "email": user.email
            }
        }, status=status.HTTP_201_CREATED)

    # 5. If the data was invalid, DRF automatically formats the errors for us
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    




@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def manage_profile(request):
    # Grab the profile connected to the logged-in user
    profile = request.user.profile 

    # 1. Handle GET request (Frontend asks: "What is my data?")
    if request.method == 'GET':
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    # 2. Handle PUT request (Frontend says: "Update my weight and goals!")
    elif request.method == 'PUT':
        # partial=True means the frontend doesn't have to send EVERY field. 
        # They can just send { "weight_kg": 80 } and it will only update that one field.
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Profile updated successfully!",
                "profile": serializer.data
            })
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    old_password = request.data.get("old_password")
    new_password = request.data.get("new_password")

    # 1. Check if the old password matches the database
    if not user.check_password(old_password):
        return Response({"error": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)

    # 2. Set the new password (this automatically hashes it!)
    user.set_password(new_password)
    user.save()

    return Response({"message": "Password updated successfully!"})    