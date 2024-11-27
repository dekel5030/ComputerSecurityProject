from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register),  # Example route for the app
    path('login/', views.login),  # Example route for the app
    path('forgot_password/', views.forgot_password),
    path('token_input/', views.token_input),  # Example route for the app
    # Example route for the app
    # Add more paths here
]