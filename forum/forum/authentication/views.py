from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.
def home(request):
    return render(request, 'authentication/main.html')
def login(request):
    return render(request, 'authentication/login.html')
def signup(request):
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

