from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name="home"),
    path('login/', views.login_user, name="login"),
    path('signup/', views.signup_user, name="signup"),
    path('logout/', views.logout_user, name="logout"),
    path('createtheme/', views.create_theme, name="createtheme"),
]