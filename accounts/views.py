from django.shortcuts import render
import os
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import Customer
from accounts.password_utils import check_password,hash

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        is_valid, message = check_password(password)
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
        print(username, password)
    return render(request, "login.html")


def forgot_password(request):
    username = request.POST['username']
    print("kaa1")
    try:
        print("kaa2")

        user = Customer.objects.get(username=username)
        email = user.email
    except ObjectDoesNotExist:
        email = False
    return render(request, "forgot_password.html")
