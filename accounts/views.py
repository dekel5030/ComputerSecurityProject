import time
import random
from django.http import HttpRequest
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.cache import cache
from datetime import datetime, timedelta
from accounts.models import User
from accounts.password_utils import check_password, login_attempt_count
from accounts.send_email import send_verification_code
import hashlib

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

        is_valid, message = check_password(password,confirm_password,username)
        if not is_valid:
            messages.error(request,message)
            return render(request, "register.html")

        if is_valid:
            user = User.objects.create_user(username=username, password=password, email=email)
            messages.success(request, "Registration successful! You can now log in.")
            return redirect('login')
        print(f"after")
    return render(request, "register.html")
# Create your views here.

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def login(request: HttpRequest):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        ip = get_client_ip(request)
        cache_key = f"failed_attempts_{ip}"
        attempts = cache.get(cache_key, 0)

        if attempts >= login_attempt_count():
            # Failed to login too many times
            return render(request, "login.html", {"error": "Tried to many times"})
        cache.set(cache_key, attempts + 1, timeout=15)
        try:
            user = User.objects.authenticate(username=username,password=password)
            if(user is not None):
                user.login(request)
                #render(request, "login.html", {"success":True})
                return redirect("home")
            else:
                return render(request, "login.html", {"error": "Incorrect password"})
        except User.DoesNotExist:
            return render(request, "login.html", {"error": "Customer does not exist"})

    return render(request, "login.html")

def logout(request):
    request.session['isLoggedIn'] = False
    request.session['username'] = None
    return redirect("login")

def is_valid_verification_code(input_code, hashed_token):
    return hash_verification_code(input_code) == hashed_token

def hash_verification_code(verification_code):
    return hashlib.sha1(verification_code.encode()).hexdigest()

def forgot_password(request):
    if request.method == "POST":
        username = request.POST['username']
        try:
            user = User.objects.get(username=username)
            verification_code = str(random.randint(100000, 999999))
            print(verification_code)
            hashed_token = hash_verification_code(verification_code)
            send_verification_code(user.email, username,  hashed_token)

            request.session['verification_code'] = hashed_token
            request.session['username'] = username
            request.session['send_time'] = datetime.now().isoformat()
            return redirect("token_input")

        except ObjectDoesNotExist:
            return render(request, "forgot_password.html", {"error": "User does not exists"})

    return render(request, "forgot_password.html")

def token_input(request):
    if request.method == "POST":
        input_token = request.POST.get('token')
        verification_code = request.session.pop('verification_code', None)
        send_time =  request.session.pop('send_time', None)
        if (datetime.now() - datetime.fromisoformat(send_time)) < timedelta(minutes=5):
            if is_valid_verification_code(input_token, verification_code):
                return redirect("reset_password")
            else:
                request.session['verification_code'] = verification_code
                request.session['send_time'] = send_time
                return render(request, "token_input.html", {"error": "Invalid Token"})
        else:
            request.session['verification_code'] = verification_code
            request.session['send_time'] = send_time
            return render(request, "token_input.html", {"error": "Token time has passed 5 minute, please send a new Token down below"})

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
            is_valid, message = check_password(password, confirm_password, user.username)
            if not is_valid:
                messages.error(request, message)
            else:
                User.objects.change_password(user, password)
                messages.success(request, "Password updated successfully")
                render(request, "reset_password.html")
                time.sleep(1)
                return redirect('login')

        except User.DoesNotExist:
            messages.error(request, "User does not exist")
            return render(request, "reset_password.html")
        except ValueError as e:
            messages.error(request, e)

    return render(request, "reset_password.html")

def change_password(request):
    if request.method == "POST":
        username = request.session.get('username', None)
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = User.objects.authenticate(username=username, password=current_password)
        print(username,current_password,new_password,user)
        if user:
            is_valid, message = check_password(new_password, confirm_password, username)
            if not is_valid:
                print("not valid password")
                messages.error(request, message)
                return render(request, "change_password.html")

            if is_valid:
                print("valid password")
                User.objects.change_password(user, new_password)
                redirect('home')
        redirect("login")

    return render(request, "change_password.html")