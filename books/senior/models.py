from django.db import models

# Create your models here.
class reg(models.Model):
    name=models.CharField(max_length=100)
    gender=models.CharField(max_length=100)
    dob=models.DateField()
    mobile=models.CharField(max_length=100)
    email=models.EmailField(max_length=100, primary_key=True)
    passwd=models.CharField(max_length=100)
    qualification=models.CharField(max_length=100)
    profession=models.CharField(max_length=100)
    ppic=models.ImageField(upload_to='static/signup/',default="")
    address=models.TextField(max_length= 100)
    city=models.CharField(max_length=100)
    yes=models.CharField(max_length=100)
    regdate=models.DateField()
    status=models.BooleanField(max_length=100)

    def __str__(self):
        return self.email

class login(models.Model):
    email=models.EmailField(max_length=100)
    password=models.CharField(max_length=100)

    def __str__(self):
        return self.email

class contact(models.Model):
        name = models.CharField(max_length=100)
        email = models.EmailField(max_length=120)
        address = models.CharField(max_length=200)
        mobile = models.CharField(max_length=20)
        message = models.TextField(max_length=600)

        def _str_(self):
            return self.name

class category(models.Model):
    cname=models.CharField(max_length=100)
    cpic=models.ImageField(upload_to='static/category/',default="")

    def __str__(self):
        return self.cname

class new(models.Model):
    newname=models.CharField(max_length=100)
    newpic=models.ImageField(upload_to='static/newrelesed/',default="")

    def __str__(self):
        return self.newname

class city(models.Model):
    cityname=models.CharField(max_length=100)
    citypic=models.ImageField(upload_to='static/city/',default="")

    def __str__(self):
        return self.cityname

class addbooks(models.Model):
    authorid=models.CharField(max_length=100)
    bookcategory=models.CharField(max_length=100)
    title=models.CharField(max_length=100)
    description=models.TextField(max_length=100)
    useful=models.CharField(max_length=100)
    coverpic=models.ImageField(upload_to='static/addbooks/',default="")
    charge=models.IntegerField()
    bookfile=models.FileField(upload_to='static/bookfiles/', blank=True, null=True)
    #uploaddate=models.DateField()

    def __str__(self):
        return self.title

