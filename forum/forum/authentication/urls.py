from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.home_page, name="home"),
    path('login/', views.login_user, name="login"),
    path('signup/', views.signup_user, name="signup"),
    path('logout/', views.logout_user, name="logout"),
    path('createtheme/', views.create_theme, name="createtheme"),
    path('creatediscussion/', views.create_discussion, name="creatediscussion"),
    path('notifications/', views.notificationspage, name="notifications"),
    path('search/', views.search, name="search"),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('<str:page>/', views.themepage),
    path('<str:page>/<str:discussionid>/', views.discussionpage)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)