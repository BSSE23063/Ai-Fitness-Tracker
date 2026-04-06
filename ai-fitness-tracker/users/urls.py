# urls.py
from django.urls import path
from .views import (
    register_user, 
    current_user, 
    manage_profile, 
    change_password
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Auth Endpoints
    path('register/', register_user, name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # User / Profile Endpoints
    path('me/', current_user, name='current_user'), # Basic user info (username, email)
    path('profile/', manage_profile, name='manage_profile'), # GET/PUT physical stats & goals
    path('change-password/', change_password, name='change_password'), # PUT new password
]