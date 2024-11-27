from django.shortcuts import render
import os
from django.core.exceptions import ObjectDoesNotExist
import ast

from accounts.models import Customer
from accounts.password_utils import check_password,hash

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        email = request.POST['email']

        is_valid, message = check_password(password,confirm_password)
        print(is_valid, message)

        if is_valid:
            salt = os.urandom(16)
            hashed_password = hash(password,salt)
            user = Customer.objects.create(username=username, password=hashed_password, email=email, salt=salt)
            print(user)

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
                return render(request, "login.html", {"error": "Incorrect username or password"})
        except Customer.DoesNotExist:
            return render(request, "login.html", {"error": "Incorrect username or password"})

    return render(request, "login.html")


def forgot_password(request):
    if request.method == "POST":
        username = request.POST['username']
        print("kaa1")
        try:
            user = Customer.objects.get(username=username)
            print("kaa2")
            email = user.email
            return token_input(request, email)
        except ObjectDoesNotExist:
            print("kaa3")
            return render(request, "forgot_password.html", {"error": "Username does not exists"})
    return render(request, "forgot_password.html")

def token_input(request, email):
    print(email)
    return render(request, "token_input.html")

