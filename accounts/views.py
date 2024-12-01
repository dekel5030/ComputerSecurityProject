from django.contrib import messages
from django.shortcuts import render
import os
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
import ast

from accounts.models import Customer
from accounts.password_utils import check_password,hash
from accounts.send_email import send_verification_code

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        email = request.POST['email']

        #validates uniqueness
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return render(request, "register.html")

        is_valid, message = check_password(password,confirm_password)
        if not is_valid:
            messages.error(request,message)
            return render(request, "register.html")

        if is_valid:
            salt = os.urandom(16)
            hashed_password = hash(password,salt)
            user = Customer.objects.create(username=username, password=hashed_password, email=email, salt=salt)
            messages.success(request, "Registration successful! You can now log in.")
            return render(request, "login.html")
        print(f"after")
    return render(request, "register.html")
# Create your views here.

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = Customer.objects.get(username=username)
            if(user.password == hash(password, ast.literal_eval(user.salt) )):
                return render(request, "login.html", {"success":True})
            else:
                return render(request, "login.html", {"error": "Incorrect password"})
        except Customer.DoesNotExist:
            return render(request, "login.html", {"error": "Customer does not exist"})

    return render(request, "login.html")


def forgot_password(request):
    if request.method == "POST":
        username = request.POST['username']
        try:
            user = Customer.objects.get(username=username)
            verification_code = generate_verification_code()
            send_verification_code(user.email, verification_code)
            return token_input(request, verification_code)

        except ObjectDoesNotExist:
            return render(request, "forgot_password.html", {"error": "User does not exists"})
    return render(request, "forgot_password.html")



def token_input(request,code):
    return render(request, "token_input.html")

def generate_verification_code():
    return 123456
