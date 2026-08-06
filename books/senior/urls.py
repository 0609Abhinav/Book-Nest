from django.urls import path
from . import views

urlpatterns=[
    path('', views.home, name='home'),
    path('home/', views.home, name='home_alt'),
    path('contactus/', views.contactus, name='contactus'),
    path('aboutus/', views.about, name='aboutus'),
    path('terms/', views.terms, name='terms'),
    path('privacy/', views.privacy, name='privacy'),
    path('signup/', views.signu, name='signup'),
    path('verify-email/', views.verify_email, name='verify_email'),
    path('signin/', views.sign, name='signin'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('addbooks/', views.addbuk, name='addbooks'),
    path('categories/', views.cat, name='categories'),
    path('latestbooks/', views.latest, name='latestbooks'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('myprofile/', views.profile, name='myprofile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('deactivate/', views.deactivate_account, name='deactivate_account'),
    path('logout/', views.logout_view, name='logout'),
    path('deletebook/<int:book_id>/', views.deletebook, name='deletebook'),
    path('toggle_wishlist/<int:book_id>/', views.toggle_wishlist, name='toggle_wishlist'),
    path('report_book/<int:book_id>/', views.report_book, name='report_book'),
]