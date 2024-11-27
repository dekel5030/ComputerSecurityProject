from django.contrib.admin import register
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),  # Example route for the app
    path('login/', views.login, name='login'),  # Example route for the app
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('token_input/', views.token_input, name='token_input')
]