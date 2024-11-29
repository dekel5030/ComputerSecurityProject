from django.core.mail import send_mail
from django.conf import settings


def send_verification_code(email, code):
    subject = 'Your Verification Code'
    message = f'Your verification code is: {code}'
    from_email = 'computerscienceproject@zohomail.com'
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)