from django.contrib import admin
from .models import *
# Register your models here.

class regAdmin(admin.ModelAdmin):
    list_display = ('name','gender','dob','mobile','email','passwd','qualification','regdate','status','profession','ppic','address','city','yes')
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

class addbooksAdmin(admin.ModelAdmin):
    list_display = ('authorid','bookcategory','title','description','useful','coverpic','charge')
admin.site.register(addbooks,addbooksAdmin)

class loginAdmin(admin.ModelAdmin):
    list_display = ('email','password')
admin.site.register(login,loginAdmin)

class contactAdmin(admin.ModelAdmin):
    list_display = ('name','email','address','mobile','message')
admin.site.register(contact,contactAdmin)