from django.shortcuts import render
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import Customer
from accounts.password_utils import check_password

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        is_Valid, message = check_password(username, password)
        print(f"Valid: {is_Valid}, message: {message}")
        email = request.POST['email']
        #user = Customer.objects.create(username=username, password=password, email=email)
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
