from django.core.mail import send_mail
from django.conf import settings

def send_email_with_parameter(request, parameter_value):
    subject = "Hello, this is a test email!"
    message = f"Your parameter value is: {parameter_value}"
    from_email = settings.DEFAULT_FROM_EMAIL  # You can set this in your settings.py
    recipient_list = ['zoko177@yahoo.com']  # Replace with actual recipient's email

    send_mail(subject, message, from_email, recipient_list)

    return 1