from django.urls import path
from . import views

urlpatterns=[
    path('',views.home),
    path('home/',views.home),
    path('contactus/',views.contactus),
    path('aboutus/',views.about),
    path('signup/',views.signu),
    path('signin/',views.sign),
    path('addbooks/',views.addbuk),
    path('categories/',views.cat),
    path('latestbooks/',views.latest),
    path('myprofile/',views.profile),
    path('logout/',views.logout),
    path('deletebook/<int:book_id>/',views.deletebook, name='deletebook'),
]