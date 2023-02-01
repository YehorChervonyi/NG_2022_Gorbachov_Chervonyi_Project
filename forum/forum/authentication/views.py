from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request, 'authentication/main.html')


# This function logging user to his account.
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.success(request, "Username or Password doesnt exist, try again...")
            return redirect('login')
    context = {}
    return render(request, 'authentication/login.html', context)


# This function will registrate user and create his account, and redirect it on home page.
def signup_user(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            return redirect('login')

    context = {'form': form}
    return render(request, 'authentication/signup.html', context)

