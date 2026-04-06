from django.urls import path
from .views import list_exercises

urlpatterns = [
    path('', list_exercises),
]