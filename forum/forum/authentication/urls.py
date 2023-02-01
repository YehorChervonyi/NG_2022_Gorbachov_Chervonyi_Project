from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.login_user, name="login"),
    path('signup/', views.signup_user, name="signup"),
    path('logout/', views.logout_user, name="logout"),
]