from django.db import connection
from django.shortcuts import render
from django.http import HttpResponse
from .models import *
import datetime


# Create your views here.

def home(request):
    cdata = category.objects.all().order_by('-id')
    citydata = city.objects.all()
    newdata = new.objects.all()
    return render(request, 'senior/index.html', {"data": cdata, "citydata": citydata, "newdata": newdata})


def contactus(request):
    status = False
    if request.method == 'POST':
        Name = request.POST.get("name", "")
        Email = request.POST.get("email", "")
        Address = request.POST.get("address", "")
        Mobile = request.POST.get("mobile", "")
        Message = request.POST.get("msg", "")
        x = contact(name=Name, email=Email, address=Address, mobile=Mobile, message=Message)
        x.save()
        status = True

    return render(request, 'senior/contactus.html', {'S': status})


def about(request):
    return render(request, 'senior/aboutus.html')


def signu(request):
    if request.method == 'POST':
        Name = request.POST.get("name", "")
        Gender = request.POST.get("gender", "")
        DOB = request.POST.get("dob", "")
        Mobile = request.POST.get("mobile", "")
        Email = request.POST.get("email", "")
        Password = request.POST.get("passwd", "")
        Highestqualification = request.POST.get("qualification", "")
        #Profession = request.POST.get("pro", "")
        Picname = request.FILES['pp']
        City = request.POST.get("city", "")
        Address = request.POST.get("address", "")
        Display = request.POST.get("yes", "")
        reg(name=Name, gender=Gender, dob=DOB, mobile=Mobile, email=Email, passwd=Password,
            qualification=Highestqualification, ppic=Picname, address=Address, city=City,
            yes=Display, regdate=datetime.datetime.now(), status=True).save()
        return HttpResponse(
            "<script>alert('You are Registered Successfully...');window.location.href='/senior/signup';</script>")

    return render(request, 'senior/signup.html')


def sign(request):
    if request.method == 'POST':
        Email = request.POST.get("email", "")
        Passwd = request.POST.get("passw", "")
        checkuser = reg.objects.filter(email=Email, passwd=Passwd)
        # print(checkuser)
        if (checkuser):
            request.session["user"] = Email
            return HttpResponse(
                "<script>alert('LOGIN SUCCESSFULLY....');window.location.href='/senior/home';</script>")

        else:
            return HttpResponse(
                "<script>alert('UserId or Password is Incorrect....');window.location.href='/senior/signin';</script>")

    return render(request, 'senior/signin.html')


def addbuk(request):
    if request.session.get('user'):
        cdata = category.objects.all()
        if request.method == 'POST':
            authotid = request.session.get('user',"")
            bookcategory = request.POST.get("category","")
            title = request.POST.get("name","")
            description = request.POST.get("short","")
            useful = request.POST.get("useful","")
            #profession=request.POST.get("profession","")
            coverpic = request.FILES['cp']
            charge = request.POST.get("charge","")
            bookfile = request.FILES.get('bf', None)
            # uploaddate=request.POST.get("charge")
            data=addbooks(authorid=authotid, bookcategory=bookcategory, title=title,description=description, useful=useful,
                     coverpic=coverpic, charge=charge, bookfile=bookfile)
            #, uploaddate = datetime.datetime.now()
            data.save()
        return render(request, 'senior/addbooks.html', {"category": cdata})
    else:
        return HttpResponse(
            "<script>alert('Please Login first to Add Books....');window.location.href='/senior/signin';</script>")


def cat(request):
    return render(request, 'senior/categories.html')


def logout(request):
    del request.session['user']
    return HttpResponse(
        "<script>alert('You are successfully LogOut....');window.location.href='/senior/home/';</script>")


def profile(request):
    if request.session.get('user'):
        id=request.session.get('user')
        bookdata=addbooks.objects.filter(authorid=id)
        return render(request, 'senior/myprofile.html',{"bookdata":bookdata})
    else:
        return HttpResponse(
            "<script>alert('Please Login first to Add Books....');window.location.href='/senior/signin';</script>")


def deletebook(request, book_id):
    if request.session.get('user'):
        user_email = request.session.get('user')
        try:
            book = addbooks.objects.get(id=book_id, authorid=user_email)
            book.delete()
            return HttpResponse(
                "<script>alert('Book deleted successfully.');window.location.href='/senior/myprofile/';</script>")
        except addbooks.DoesNotExist:
            return HttpResponse(
                "<script>alert('Book not found or you do not have permission.');window.location.href='/senior/myprofile/';</script>")
    else:
        return HttpResponse(
            "<script>alert('Please login first.');window.location.href='/senior/signin/';</script>")


def latest(request):
    cursor = connection.cursor()
    if request.GET.get('id') is None:
        cursor.execute("select b.*,u.* from senior_addbooks b, senior_reg u where b.authorid=u.email")
    else:
        id = request.GET.get('id')
        cursor.execute("select b.*,u.* from senior_addbooks b, senior_reg u where b.authorid=u.email and b.bookcategory=%s", [id])
    Addbooks = cursor.fetchall()
    cdata = category.objects.all().order_by('-id')
    return render(request, 'senior/latestbooks.html', {"bdetail": Addbooks, "data": cdata})

