from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from . forms import RegisterUserForm
from django.contrib.auth.models import User


# Create your views here.
def home_page(request):
    return render(request, 'authentication/main.html')


# This function logging user to his account.
def login_user(request):
    if request.method == "POST":
        username = request.POST['username'].strip()
        password = request.POST['password'].strip()
        # username = User.objects.get(email=email.lower()).username
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            if username == "" and password == "":
                messages.warning(request, "Username and Password text areas are empty")
            elif username == "":
                messages.warning(request, "Username text area is empty")
            elif password == "":
                messages.warning(request, "Password text area is empty")
            else:
                messages.warning(request, "Username or Password doesnt exist, try again...")

    context = {}
    return render(request, 'authentication/login.html', context)


# This function will registrate user and create his account, and redirect it on home page.
def signup_user(request):
    form = RegisterUserForm()

    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, "Registration successful")
            return redirect('login')

    context = {'form': form}
    return render(request, 'authentication/signup.html', context)


def logout_user(request):
    logout(request)
    messages.info(request, "You are logged out")
    return redirect('home')

