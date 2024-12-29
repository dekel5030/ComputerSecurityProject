from django.contrib.admin import register
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),  # Example route for the app
    path('login/', views.login, name='login'),  # Example route for the app
    path('forgot_password/', views.forgot_password, name='forgot_password'),  # Example route for the app
    path('change_password/', views.change_password, name='change_password'),
    path('token/', views.token_input, name='token_input'),
    path('reset_password/', views.reset_password, name='reset_password'),
    # Add more paths here
]