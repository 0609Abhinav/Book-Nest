import random
import string
import requests
import json
import os
from django.conf import settings
from .models import EmailOTP

def generate_otp(length=6):
    return ''.join(random.choices(string.digits, k=length))

def send_otp_email(email):
    otp = generate_otp()
    EmailOTP.objects.create(email=email, otp=otp)
    
    api_key = os.environ.get('BREVO_SMTP_KEY')
    sender_email = os.environ.get('BREVO_SMTP_USER', 'noreply@booknest.local')
    
    if api_key:
        url = "https://api.brevo.com/v3/smtp/email"
        headers = {
            "accept": "application/json",
            "api-key": api_key,
            "content-type": "application/json"
        }
        data = {
            "sender": {"name": "BookNest", "email": sender_email},
            "to": [{"email": email}],
            "subject": "Your BookNest OTP",
            "htmlContent": f"<html><body style='font-family:sans-serif;'><h3>Welcome to BookNest!</h3><p>Your verification code is <strong style='color:#00b4d8;font-size:24px;'>{otp}</strong></p><p>It will expire soon.</p></body></html>"
        }
        try:
            # Using Brevo API via HTTPS because PythonAnywhere free tier blocks SMTP (port 587)
            requests.post(url, headers=headers, data=json.dumps(data), timeout=10)
        except Exception as e:
            print(f"Brevo API error: {e}")
    else:
        # Fallback to local console if keys are missing
        print(f"--- OTP FOR {email}: {otp} ---")
        
    return True

def verify_otp(email, otp):
    try:
        otp_record = EmailOTP.objects.filter(email=email, otp=otp, is_used=False).latest('created_at')
        otp_record.is_used = True
        otp_record.save()
        return True
    except EmailOTP.DoesNotExist:
        return False
