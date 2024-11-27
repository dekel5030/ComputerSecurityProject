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
            return render(request, "login.html", {"error": "Customer does not exist"})

    return render(request, "login.html")


def forgot_password(request):
    if request.method == "POST":
        username = request.POST['username']
        print("kaa1")
        try:
            print("kaa2")

            user = Customer.objects.get(username=username)
            email = user.email
        except ObjectDoesNotExist:
            email = False
    return render(request, "forgot_password.html")
