from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import *
from .decorators import login_required_custom, rate_limit
from .validators import validate_image_file, validate_pdf_file
from .utils import send_otp_email, verify_otp

def home(request):
    cdata = category.objects.all().order_by('-id')
    citydata = city.objects.all()
    newdata = new.objects.all()
    featured_books = addbooks.objects.all().order_by('-created_at')[:10]
    return render(request, 'senior/index.html', {
        "data": cdata, 
        "citydata": citydata, 
        "newdata": newdata,
        "featured_books": featured_books
    })

@rate_limit('contact', 5, 3600)
def contactus(request):
    if request.method == 'POST':
        Name = request.POST.get("name", "")
        Email = request.POST.get("email", "")
        Address = request.POST.get("address", "")
        Mobile = request.POST.get("mobile", "")
        Message = request.POST.get("msg", "")
        contact.objects.create(name=Name, email=Email, address=Address, mobile=Mobile, message=Message)
        messages.success(request, "Your message has been sent successfully!")
        return redirect('/senior/contactus/')
    return render(request, 'senior/contactus.html')

def about(request):
    return render(request, 'senior/aboutus.html')

def terms(request):
    return render(request, 'senior/terms.html')

def privacy(request):
    return render(request, 'senior/privacy.html')

@rate_limit('signup', 5, 3600)
def signu(request):
    if request.method == 'POST':
        Email = request.POST.get("email", "")
        if reg.objects.filter(email=Email).exists():
            messages.error(request, "Email is already registered.")
            return redirect('/senior/signup/')
            
        Name = request.POST.get("name", "")
        Gender = request.POST.get("gender", "")
        DOB = request.POST.get("dob", "")
        Mobile = request.POST.get("mobile", "")
        Password = request.POST.get("passwd", "")
        CPassword = request.POST.get("cpasswd", "")
        
        if Password != CPassword:
            messages.error(request, "Passwords do not match.")
            return redirect('/senior/signup/')

        Highestqualification = request.POST.get("qualification", "")
        Profession = request.POST.get("profession", "")
        Picname = request.FILES.get('pp')
        City = request.POST.get("city", "")
        Address = request.POST.get("address", "")
        Display = request.POST.get("dp", "no")

        if Picname:
            try:
                validate_image_file(Picname)
            except ValidationError as e:
                messages.error(request, str(e))
                return redirect('/senior/signup/')

        hashed_password = make_password(Password)
        
        reg.objects.create(
            name=Name, gender=Gender, dob=DOB, mobile=Mobile, email=Email, passwd=hashed_password,
            qualification=Highestqualification, profession=Profession, ppic=Picname, 
            address=Address, city=City, yes=Display, is_active=True, is_verified=False
        )
        
        send_otp_email(Email)
        request.session['verify_email'] = Email
        messages.success(request, "OTP sent to your email. Please verify.")
        return redirect('verify_email')

    return render(request, 'senior/signup.html')

def verify_email(request):
    email = request.session.get('verify_email')
    if not email:
        return redirect('signup')

    if request.method == 'POST':
        otp = request.POST.get('otp')
        if verify_otp(email, otp):
            user = reg.objects.get(email=email)
            user.is_verified = True
            user.save()
            del request.session['verify_email']
            messages.success(request, "Email verified! You can now log in.")
            return redirect('signin')
        else:
            messages.error(request, "Invalid or expired OTP.")
    return render(request, 'senior/verify_email.html', {'email': email})

@rate_limit('login', 10, 3600)
def sign(request):
    if request.method == 'POST':
        Email = request.POST.get("email", "")
        Passwd = request.POST.get("passw", "")
        
        try:
            user = reg.objects.get(email=Email)
            if not user.is_active:
                messages.error(request, "Your account is deactivated.")
            elif not user.is_verified:
                messages.warning(request, "Please verify your email first.")
                request.session['verify_email'] = Email
                send_otp_email(Email)
                return redirect('verify_email')
            elif check_password(Passwd, user.passwd):
                request.session["user"] = Email
                request.session.set_expiry(1209600) # 2 weeks login persistence
                messages.success(request, "Login successful!")
                return redirect('home')
            else:
                messages.error(request, "Incorrect password.")
        except reg.DoesNotExist:
            messages.error(request, "User not found.")

        return redirect('signin')

    return render(request, 'senior/signin.html')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if reg.objects.filter(email=email).exists():
            send_otp_email(email)
            request.session['reset_email'] = email
            messages.success(request, "OTP sent to your email.")
            return redirect('reset_password')
        messages.error(request, "Email not found.")
    return render(request, 'senior/forgot_password.html')

def reset_password(request):
    email = request.session.get('reset_email')
    if not email:
        return redirect('forgot_password')

    if request.method == 'POST':
        otp = request.POST.get('otp')
        new_pass = request.POST.get('new_password')
        if verify_otp(email, otp):
            user = reg.objects.get(email=email)
            user.passwd = make_password(new_pass)
            user.save()
            del request.session['reset_email']
            messages.success(request, "Password reset successfully. You can log in.")
            return redirect('signin')
        messages.error(request, "Invalid or expired OTP.")
    return render(request, 'senior/reset_password.html', {'email': email})

@login_required_custom
def addbuk(request):
    cdata = category.objects.all()
    if request.method == 'POST':
        authotid = request.session.get('user')
        bookcategory = request.POST.get("category", "")
        title = request.POST.get("name", "")
        
        if addbooks.objects.filter(title__iexact=title).exists():
            messages.error(request, "A book with this title already exists.")
            return redirect('addbooks')

        description = request.POST.get("short", "")
        useful = request.POST.get("useful", "")
        charge = request.POST.get("charge", "")
        coverpic = request.FILES.get('cp')
        bookfile = request.FILES.get('bf')

        try:
            if coverpic:
                validate_image_file(coverpic)
            if bookfile:
                validate_pdf_file(bookfile)
        except ValidationError as e:
            messages.error(request, str(e))
            return redirect('addbooks')

        addbooks.objects.create(
            authorid=authotid, bookcategory=bookcategory, title=title, 
            description=description, useful=useful, coverpic=coverpic, 
            charge=charge, bookfile=bookfile, status='approved'
        )
        messages.success(request, "Book added successfully!")
        return redirect('myprofile')

    return render(request, 'senior/addbooks.html', {"category": cdata})

def cat(request):
    return render(request, 'senior/categories.html')

def logout_view(request):
    if 'user' in request.session:
        del request.session['user']
        messages.success(request, "Logged out successfully.")
    return redirect('home')

@login_required_custom
def profile(request):
    user_email = request.session.get('user')
    bookdata = addbooks.objects.filter(authorid=user_email)
    user_info = reg.objects.get(email=user_email)
    
    wishlist_records = Wishlist.objects.filter(user_email=user_email)
    wishlist_books = []
    for w in wishlist_records:
        try:
            book = addbooks.objects.get(id=w.book_id)
            wishlist_books.append(book)
        except addbooks.DoesNotExist:
            continue

    return render(request, 'senior/myprofile.html', {
        "bookdata": bookdata, 
        "user_info": user_info,
        "wishlist_books": wishlist_books
    })

@login_required_custom
def profile_edit(request):
    user_email = request.session.get('user')
    user = reg.objects.get(email=user_email)
    
    if request.method == 'POST':
        user.name = request.POST.get("name", user.name)
        user.city = request.POST.get("city", user.city)
        user.mobile = request.POST.get("mobile", user.mobile)
        
        pic = request.FILES.get('pp')
        if pic:
            try:
                validate_image_file(pic)
                user.ppic = pic
            except ValidationError as e:
                messages.error(request, str(e))
                return redirect('profile_edit')
        
        user.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('myprofile')

    return render(request, 'senior/profile_edit.html', {"user_info": user})

@login_required_custom
def deactivate_account(request):
    if request.method == 'POST':
        user_email = request.session.get('user')
        user = reg.objects.get(email=user_email)
        user.is_active = False
        user.save()
        del request.session['user']
        messages.success(request, "Account deactivated successfully.")
        return redirect('home')
    return render(request, 'senior/deactivate.html')

@login_required_custom
def deletebook(request, book_id):
    user_email = request.session.get('user')
    try:
        book = addbooks.objects.get(id=book_id, authorid=user_email)
        book.delete()
        messages.success(request, "Book deleted successfully.")
    except addbooks.DoesNotExist:
        messages.error(request, "Book not found or unauthorized.")
    return redirect('myprofile')

def latest(request):
    cdata = category.objects.all().order_by('-id')
    cat_id = request.GET.get('id')
    sort_by = request.GET.get('sort', '-created_at')
    search_query = request.GET.get('q')
    
    books_query = addbooks.objects.filter(status='approved')
    if cat_id:
        books_query = books_query.filter(bookcategory=cat_id)
        
    if search_query:
        from django.db.models import Q
        books_query = books_query.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
        
    if sort_by == 'price_asc':
        books_query = books_query.order_by('charge')
    elif sort_by == 'price_desc':
        books_query = books_query.order_by('-charge')
    elif sort_by == 'downloads':
        books_query = books_query.order_by('-download_count')
    else:
        books_query = books_query.order_by('-created_at')
        
    user_email = request.session.get('user')
    user_wishlist_books = set()
    if user_email:
        user_wishlist_books = set(Wishlist.objects.filter(user_email=user_email).values_list('book_id', flat=True))
        
    books_data = []
    for book in books_query:
        in_wishlist = book.id in user_wishlist_books
        try:
            seller = reg.objects.get(email=book.authorid)
            books_data.append({'book': book, 'seller': seller, 'in_wishlist': in_wishlist})
        except reg.DoesNotExist:
            books_data.append({'book': book, 'seller': None, 'in_wishlist': in_wishlist})

    return render(request, 'senior/latestbooks.html', {"bdetail": books_data, "data": cdata, "current_cat": cat_id, "current_sort": sort_by})

def book_detail(request, book_id):
    try:
        book = addbooks.objects.get(id=book_id, status='approved')
        seller = reg.objects.get(email=book.authorid)
        related_books = addbooks.objects.filter(bookcategory=book.bookcategory, status='approved').exclude(id=book_id)[:4]
        
        # If logged in, check wishlist
        in_wishlist = False
        if 'user' in request.session:
            in_wishlist = Wishlist.objects.filter(user_email=request.session['user'], book_id=book_id).exists()
            
        return render(request, 'senior/book_detail.html', {
            'book': book, 
            'seller': seller, 
            'related_books': related_books,
            'in_wishlist': in_wishlist
        })
    except (addbooks.DoesNotExist, reg.DoesNotExist):
        messages.error(request, "Book not found.")
        return redirect('latestbooks')

# --- Phase 1: Security & Auth View Implementations ---

def verify_email(request):
    if request.method == 'POST':
        email = request.session.get('pending_email')
        otp = request.POST.get('otp')
        try:
            otp_record = EmailOTP.objects.get(email=email, otp=otp, is_used=False)
            # Mark OTP as used
            otp_record.is_used = True
            otp_record.save()
            
            # Activate user
            user = reg.objects.get(email=email)
            user.is_verified = True
            user.is_active = True
            user.save()
            
            messages.success(request, "Email verified successfully! You can now log in.")
            return redirect('signin')
        except EmailOTP.DoesNotExist:
            messages.error(request, "Invalid or expired OTP.")
    return render(request, 'senior/verify_email.html')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = reg.objects.get(email=email)
            # Create OTP
            import random
            otp_code = str(random.randint(100000, 999999))
            EmailOTP.objects.create(email=email, otp=otp_code)
            
            # Send Email
            send_mail(
                'Password Reset OTP',
                f'Your password reset OTP is {otp_code}',
                'webmaster@localhost',
                [email],
                fail_silently=False,
            )
            request.session['reset_email'] = email
            return redirect('reset_password')
        except reg.DoesNotExist:
            messages.error(request, "No account found with this email.")
    return render(request, 'senior/forgot_password.html')

def reset_password(request):
    if request.method == 'POST':
        email = request.session.get('reset_email')
        otp = request.POST.get('otp')
        new_password = request.POST.get('new_password')
        
        try:
            otp_record = EmailOTP.objects.get(email=email, otp=otp, is_used=False)
            otp_record.is_used = True
            otp_record.save()
            
            user = reg.objects.get(email=email)
            user.passwd = new_password
            user.save()
            
            # Also update login model
            login_obj = login.objects.get(email=email)
            login_obj.password = new_password
            login_obj.save()
            
            messages.success(request, "Password reset successfully! Please log in.")
            return redirect('signin')
        except (EmailOTP.DoesNotExist, reg.DoesNotExist, login.DoesNotExist):
            messages.error(request, "Invalid OTP or error resetting password.")
            
    return render(request, 'senior/reset_password.html')

def profile_edit(request):
    if 'user' not in request.session:
        return redirect('signin')
        
    user_email = request.session['user']
    user = reg.objects.get(email=user_email)
    
    if request.method == 'POST':
        user.name = request.POST.get('name')
        user.mobile = request.POST.get('mobile')
        user.city = request.POST.get('city')
        if 'pp' in request.FILES:
            user.ppic = request.FILES['pp']
        user.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('myprofile')
        
    return render(request, 'senior/profile_edit.html', {'user_info': user})

def deactivate_account(request):
    if 'user' not in request.session:
        return redirect('signin')
        
    if request.method == 'POST':
        user_email = request.session['user']
        user = reg.objects.get(email=user_email)
        user.is_active = False
        user.save()
        
        # Deactivate their books
        addbooks.objects.filter(authorid=user_email).update(status='rejected')
        
        del request.session['user']
        messages.success(request, "Your account has been deactivated.")
        return redirect('home')
        
    return render(request, 'senior/deactivate.html')

def logout_view(request):
    if 'user' in request.session:
        del request.session['user']
    messages.success(request, "You have been logged out.")
    return redirect('home')

def book_detail(request, book_id):
    try:
        book = addbooks.objects.get(id=book_id, status='approved')
        seller = reg.objects.filter(email=book.authorid).first()
        related_books = addbooks.objects.filter(bookcategory=book.bookcategory, status='approved').exclude(id=book_id)[:4]
        return render(request, 'senior/book_detail.html', {'book': book, 'seller': seller, 'related_books': related_books})
    except addbooks.DoesNotExist:
        messages.error(request, "Book not found or pending review.")
        return redirect('latestbooks')

@login_required_custom
def toggle_wishlist(request, book_id):
    if request.method == 'POST':
        user_email = request.session.get('user')
        wishlist_item = Wishlist.objects.filter(user_email=user_email, book_id=book_id).first()
        if wishlist_item:
            wishlist_item.delete()
            messages.success(request, "Removed from wishlist.")
        else:
            Wishlist.objects.create(user_email=user_email, book_id=book_id)
            messages.success(request, "Added to wishlist.")
    return redirect('book_detail', book_id=book_id)

@login_required_custom
def report_book(request, book_id):
    if request.method == 'POST':
        reason = request.POST.get('reason', 'Inappropriate content')
        user_email = request.session.get('user')
        BookReport.objects.create(book_id=book_id, reporter_email=user_email, reason=reason)
        messages.success(request, "Thank you. This book has been reported to the admins.")
    return redirect('book_detail', book_id=book_id)
