from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from . forms import RegisterUserForm, User, ThemeForm, DiscussionForm


# Create your views here.
def home_page(request):
    return render(request, 'authentication/main.html')

# This function logging user to his account.
def login_user(request):
    if request.method == "POST":
        email = request.POST['email'].strip()
        password = request.POST['password'].strip()
        # username = User.objects.get(email=email.lower()).username
        try:
            get_user = User.objects.get(email=email)
        except:
            get_user = None

        user = authenticate(request, username=get_user, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            if email == "" and password == "":
                messages.warning(request, "Email and Password text areas are empty")
            elif email == "":
                messages.warning(request, "Email text area is empty")
            elif password == "":
                messages.warning(request, "Password text area is empty")
            else:
                messages.warning(request, "Email or Password doesnt exist, try again...")

    context = {}
    return render(request, 'authentication/login.html', context)


# This function will registrate user and create his account, and redirect it on home page.
def signup_user(request):
    form = RegisterUserForm()

    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = user.email.lower()
            user.save()
            messages.success(request, "Registration successful")
            return redirect('login')

    context = {'form': form}
    return render(request, 'authentication/signup.html', context)


def logout_user(request):
    logout(request)
    messages.info(request, "You are logged out")
    return redirect('home')

def create_theme(request):
    form = ThemeForm
    context = {'form': form}
    return render(request, 'authentication/createtheme.html', context)

def create_discussion(request):
    form = DiscussionForm
    context = {'form': form}
    return render(request, 'authentication/creatediscussion.html', context)
