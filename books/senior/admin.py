from django.contrib import admin
from django.utils.html import format_html
from .models import *

class regAdmin(admin.ModelAdmin):
    list_display = ('name','email','mobile','city','is_active','is_verified','created_at')
    list_filter = ('is_active', 'is_verified', 'city')
    search_fields = ('name', 'email', 'mobile')
admin.site.register(reg,regAdmin)

class categoryAdmin(admin.ModelAdmin):
    list_display = ('cname','cpic')
admin.site.register(category,categoryAdmin)

class newAdmin(admin.ModelAdmin):
    list_display = ('newname','newpic')
admin.site.register(new,newAdmin)

class cityAdmin(admin.ModelAdmin):
    list_display = ('cityname','citypic')
admin.site.register(city,cityAdmin)

@admin.action(description='Approve selected books')
def approve_books(modeladmin, request, queryset):
    queryset.update(status='approved')

@admin.action(description='Reject selected books')
def reject_books(modeladmin, request, queryset):
    queryset.update(status='rejected')

class addbooksAdmin(admin.ModelAdmin):
    list_display = ('title', 'authorid', 'bookcategory', 'charge', 'status', 'created_at')
    list_filter = ('status', 'bookcategory', 'created_at')
    search_fields = ('title', 'authorid')
    list_editable = ('status',)
    actions = [approve_books, reject_books]
admin.site.register(addbooks,addbooksAdmin)

class loginAdmin(admin.ModelAdmin):
    list_display = ('email','password')
admin.site.register(login,loginAdmin)

class contactAdmin(admin.ModelAdmin):
    list_display = ('name','email','mobile','created_at')
    search_fields = ('name', 'email')
admin.site.register(contact,contactAdmin)

# New Models
@admin.register(EmailOTP)
class EmailOTPAdmin(admin.ModelAdmin):
    list_display = ('email', 'otp', 'is_used', 'created_at')
    list_filter = ('is_used', 'created_at')

@admin.register(BookReport)
class BookReportAdmin(admin.ModelAdmin):
    list_display = ('book_id', 'reporter_email', 'is_resolved', 'created_at')
    list_filter = ('is_resolved', 'created_at')

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'book_id', 'added_at')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book_id', 'reviewer_email', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'subscribed_at')
    list_filter = ('is_active', 'subscribed_at')