import os
import django
import datetime

def run_setup():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'books.settings')
    django.setup()
    
    from senior.models import reg, category
    from django.contrib.auth.hashers import make_password
    
    # 1. Add "Live Book" category
    category.objects.get_or_create(cname='Live Book')
    print("✅ 'Live Book' category successfully added.")
    
    # 2. Create Demo User Account
    email = 'demo@booknest.in'
    password = 'demo_password'
    
    user, created = reg.objects.get_or_create(
        email=email,
        defaults={
            'name': 'Demo User',
            'gender': 'Other',
            'dob': datetime.date(2000, 1, 1),
            'mobile': '0000000000',
            'passwd': make_password(password),
            'qualification': 'Demo',
            'profession': 'Reviewer',
            'address': 'PythonAnywhere',
            'city': 'Cloud',
            'yes': 'yes',
            'is_active': True,
            'is_verified': True
        }
    )
    
    if created:
        print(f"✅ Demo user created! Email: {email} | Password: {password}")
    else:
        # If user already exists, let's update their password and make sure they are active
        user.passwd = make_password(password)
        user.is_active = True
        user.is_verified = True
        user.save()
        print(f"✅ Demo user updated! Email: {email} | Password: {password}")

if __name__ == '__main__':
    run_setup()
