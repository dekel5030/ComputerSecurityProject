from django.contrib import messages
from django.shortcuts import render
import os
from django.contrib import messages
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
import ast
import random

from django.template.context_processors import request

from accounts.models import User
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
            messages.error(request, "Username is already taken")
            return render(request, "register.html")

        is_valid, message = check_password(password,confirm_password)
        if not is_valid:
            messages.error(request,message)
            return render(request, "register.html")

        if is_valid:
            '''salt = os.urandom(16)
            hashed_password = hash(password,salt)
            user = User.objects.create(username=username, password=hashed_password, email=email, salt=salt.hex())'''

            # instead this ↑↑↑↑↑↑↑↑↑↑ do this ↓↓↓↓↓↓↓↓↓↓

            user = User.objects.create_user(username=username, password=password, email=email)

            messages.success(request, "Registration successful! You can now log in.")
            return redirect('login')
        print(f"after")
    return render(request, "register.html")
# Create your views here.

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
            if(user.password == hash(password, bytes.fromhex(user.salt) )):
                user = authenticate(request, username=username, password=password)
                return render(request, "login.html", {"success":True})
            else:
                return render(request, "login.html", {"error": "Incorrect password"})
        except User.DoesNotExist:
            return render(request, "login.html", {"error": "Customer does not exist"})

    return render(request, "login.html")


def forgot_password(request):
    if request.method == "POST":
        username = request.POST['username']
        try:
            user = User.objects.get(username=username)
            verification_code = generate_verification_code()
            print(verification_code)
            send_verification_code(user.email, username,  verification_code)

            request.session['verification_code'] = verification_code
            request.session['username'] = username
            return redirect("token_input")

        except ObjectDoesNotExist:
            return render(request, "forgot_password.html", {"error": "User does not exists"})

    return render(request, "forgot_password.html")

def token_input(request):
    if request.method == "POST":
        input_token = request.POST.get('token')
        verification_code = request.session.pop('verification_code', None)

        if input_token == verification_code:
            return redirect("reset_password")
        else:
            print("invalid token")

def home(request):
    return render(request);

def token_input(request,code):
    return render(request, "token_input.html")

def reset_password(request):
    if request.method == "POST":
        username = request.session.get('username', None)
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if(username == None):
            return redirect("forgot_password")

        try:
            user = User.objects.get(username=username)
            is_valid, message = check_password(password, confirm_password)
            if not is_valid:
                messages.error(request, message)
            else:
                User.objects.change_password(user, password)
                messages.success(request, "Password updated successfully")
                render(request, "reset_password.html")
            #return render(request, "login.html")

        except User.DoesNotExist:
            messages.error(request, "User does not exist")
            return render(request, "reset_password.html")



    return render(request, "reset_password.html")


def generate_verification_code():
    return 123456

def change_password(request):
    if request.method == "GET":return render(request, "change_password.html",{})
