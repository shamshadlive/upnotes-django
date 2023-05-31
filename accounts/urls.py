from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.login_page, name="login_page"),
    path("logout/", views.logout_page, name="logout_page"),
    path("register/", views.register, name="register"),
    
    #admin
    
    path("admincontrol/login", views.admincontrolLogin, name="admin_login"),
    path("admincontrol/register", views.admincontrolRegister, name="admin_register"),
   
    
    
]