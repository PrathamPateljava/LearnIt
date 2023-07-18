from django.core.mail import send_mail
import random
import re

def generate_otp():
    return random.randint(000000,999999)
def send_otp(mail,otp):
    send_mail(
        'Verification OTP',
        f'Your Verification OTP is {otp}.',
        'learnit.django@gmail.com',
        [mail],
        fail_silently=False,
    )
def send_confirmation(mail,title):
    send_mail(
        f"Buying Course: {title}",
        f"Your payment for the Course: {title} was done successfully. Thank You for joining us.\n\n Happy Learning!!",
        'learnit.django@gmail.com',
        [mail],
        fail_silently=False
    )
def check_email_exists(email):
        pattern = r"^[a-zA-Z0-9._%+-]+@gmail\.com$"
        if re.match(pattern, email):
            return True
        else:
            return False

def get_upload_path(instance, filename):
    return "uploads/{}/{}".format(instance.topic, filename)