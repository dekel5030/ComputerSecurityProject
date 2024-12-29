import os
import json
import re
from hashlib import pbkdf2_hmac


def hash(password,salt):
    our_app_iters = 500_000  # Application specific, read above.
    dk = pbkdf2_hmac('sha256', bytes(password, 'utf-8'), salt * 2, our_app_iters)
    return dk.hex()


def load_config():
    # Path to your config.json file
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')

    with open(config_path, 'r') as file:
        config = json.load(file)

    return config

config = load_config()

def login_attempt_count():
    return config["login_attempts"]

def check_password(password,confirm_password, username):
    if password != confirm_password:
        return False, "The passwords do not match"

    if is_password_too_short(password):
        return False, f"The password is too short. It must be at least {config['password_length']} characters long."

    if config["password_complexity"]["uppercase"]:
        if not has_uppercase(password):
            return False, "The password must contain at least one uppercase letter."

    if config["password_complexity"]["lowercase"]:
        if not has_lowercase(password):
            return False, "The password must contain at least one lowercase letter."

    if config["password_complexity"]["numbers"]:
        if not has_numbers(password):
            return False, "The password must contain at least one numeric digit."

    if config["password_complexity"]["special_characters"]:
        if not has_special_characters(password):
            return False, "The password must contain at least one special character."



    if len(config["dictionary_restriction"]) > 0:
        if is_restricted(password):
            return False, f"The password cannot be any of the following: {config['dictionary_restriction']}"

    return True, "The password meets all requirements."


# Returns true if the password is too short
def is_password_too_short(password):
    return (len(password) < config['password_length'])

def has_uppercase(password):
    return bool(re.search(r'[A-Z]', password))

def has_lowercase(password):
    return bool(re.search(r'[a-z]', password))

def has_numbers(password):
    return bool(re.search(r'[0-9]', password))

def has_special_characters(password):
    return bool(re.search(r'[^a-zA-Z0-9]', password))

def is_restricted(password):
    if(password in config['dictionary_restriction']):
        return True

