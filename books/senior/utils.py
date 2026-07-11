import random
import string
from django.core.mail import send_mail
from django.conf import settings
from .models import EmailOTP

def generate_otp(length=6):
    return ''.join(random.choices(string.digits, k=length))

def send_otp_email(email):
    otp = generate_otp()
    EmailOTP.objects.create(email=email, otp=otp)
    subject = 'Your BookNest OTP'
    message = f'Your verification code is {otp}. It will expire soon.'
    email_from = getattr(settings, 'EMAIL_HOST_USER', 'noreply@booknest.local')
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True

def verify_otp(email, otp):
    try:
        otp_record = EmailOTP.objects.filter(email=email, otp=otp, is_used=False).latest('created_at')
        otp_record.is_used = True
        otp_record.save()
        return True
    except EmailOTP.DoesNotExist:
        return False
