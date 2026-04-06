# serializers.py
from rest_framework import serializers
from .models import User
from .models import Profile

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True) # Ensures password is never sent back in API responses

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        # create_user automatically hashes the password!
        user = User.objects.create_user(**validated_data)
        return user
    
    
    
    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        # We don't include 'id' or 'user' because the user shouldn't be able to change those!
        fields = ['age', 'height_cm', 'weight_kg', 'fitness_goal', 'experience_level']    