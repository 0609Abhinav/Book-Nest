from django.db import models
from django.utils import timezone

class reg(models.Model):
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    dob = models.DateField()
    mobile = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, primary_key=True)
    passwd = models.CharField(max_length=255) # Increased max_length for hashed passwords
    qualification = models.CharField(max_length=100)
    profession = models.CharField(max_length=100)
    ppic = models.ImageField(upload_to='static/signup/', default="")
    address = models.TextField(max_length=100)
    city = models.CharField(max_length=100)
    yes = models.CharField(max_length=100)
    regdate = models.DateField(default=timezone.now)
    status = models.BooleanField(max_length=100, default=True)
    
    # New fields for security
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.email

class login(models.Model):
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.email

class contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=120)
    address = models.CharField(max_length=200)
    mobile = models.CharField(max_length=20)
    message = models.TextField(max_length=600)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

class category(models.Model):
    cname = models.CharField(max_length=100)
    cpic = models.ImageField(upload_to='static/category/', default="")

    def __str__(self):
        return self.cname

class new(models.Model):
    newname = models.CharField(max_length=100)
    newpic = models.ImageField(upload_to='static/newrelesed/', default="")

    def __str__(self):
        return self.newname

class city(models.Model):
    cityname = models.CharField(max_length=100)
    citypic = models.ImageField(upload_to='static/city/', default="")

    def __str__(self):
        return self.cityname

class addbooks(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    authorid = models.CharField(max_length=100)
    bookcategory = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=100)
    useful = models.CharField(max_length=100)
    coverpic = models.ImageField(upload_to='static/addbooks/', default="")
    charge = models.IntegerField()
    bookfile = models.FileField(upload_to='static/bookfiles/', blank=True, null=True)
    
    # New fields for moderation and tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    download_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.title

# New Models for Phase 1 & 2

class EmailOTP(models.Model):
    email = models.EmailField(max_length=100)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.email} - {self.otp}"

class BookReport(models.Model):
    book_id = models.IntegerField()
    reporter_email = models.EmailField(max_length=100)
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"Report on Book {self.book_id}"

class Wishlist(models.Model):
    user_email = models.EmailField(max_length=100)
    book_id = models.IntegerField()
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user_email', 'book_id')

class Review(models.Model):
    book_id = models.IntegerField()
    reviewer_email = models.EmailField(max_length=100)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email
