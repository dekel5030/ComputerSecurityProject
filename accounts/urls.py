from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register),  # Example route for the app
    path('login/', views.login),  # Example route for the app
    # Add more paths here
]