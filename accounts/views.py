import os
import json
import re
from tempfile import template

from django.shortcuts import render
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import Customer


def load_config():
    # Path to your config.json file
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')

    with open(config_path, 'r') as file:
        config = json.load(file)

    return config

config = load_config()
print('kaa')
def register(request):
    if request.method == "POST":
        conf = load_config()
        username = request.POST['username']
        password = request.POST['password']
        check_password(request, password)
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
    if request.method == "POST":
        print("hey")
    return render(request, "forgot_password.html")

def check_password(request, password):
    if(check_pass_len(password)):
        messages.error(request, 'the pass too short')
        print("he pass too short")

def check_pass_len(password):
    return (len(password) < config['password_length'])

def has_capital_letter(password):
    return bool(re.search(r'[A-Z]', password))

def has_lower_letter(password):
    return bool(re.search(r'[a-z]', password))

def has_numbers(password):
    return bool(re.search(r'[0-9]', password))

def has_special_charcters(password):
    return bool(re.search(r'[^a-zA-Z0-9]', password))

def is_restricted(password):
    if(password in config['restricted_words']):
        return True


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

