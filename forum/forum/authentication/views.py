from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from . forms import RegisterUserForm, User, ThemeForm, DiscussionForm
from . models import Theme, Discussion




# Create your views here.
def home_page(request):
    themes = Theme.objects.all()
    discussions=Discussion.objects.all()
    context={
        'discussions':discussions,
        'themes':themes
    }
    return render(request, 'authentication/main.html', context)

# This function logging user to his account.
def login_user(request):
    themes = Theme.objects.all()
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

    context = {
        'themes':themes
    }
    return render(request, 'authentication/login.html', context)


# This function will registrate user and create his account, and redirect it on home page.
def signup_user(request):
    themes = Theme.objects.all()
    form = RegisterUserForm()

    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = user.email.lower()
            user.save()
            messages.success(request, "Registration successful")
            return redirect('login')

    context = {
        'form': form,
        'themes':themes}
    return render(request, 'authentication/signup.html', context)


def logout_user(request):
    themes = Theme.objects.all()
    logout(request)
    messages.info(request, "You are logged out")
    return redirect('home')

def create_theme(request):
    themes = Theme.objects.all()
    
    form = ThemeForm
    if request.method == "POST":
        form = ThemeForm(request.POST)
        if form.is_valid():
            theme = form.save(commit=False)
            theme.save()
            messages.success(request, "Theme created")
            return redirect('home')
        else:
            messages.warning(request, "Theme with this name already exist")
        themes = Theme.objects.all()
    context = {'form': form,
        'themes':themes}
    return render(request, 'authentication/createtheme.html', context)

def create_discussion(request):
    themes = Theme.objects.all()
    form = DiscussionForm
    if request.method == "POST":
        form = DiscussionForm(request.POST)
        if form.is_valid():
            discussion = form.save(commit=False)
            discussion.save()
            messages.success(request, "Discussion created. We believe you wil enjoy")
            return redirect('home')
    context = {'form': form,
                'themes': themes}
    return render(request, 'authentication/creatediscussion.html', context)

def discusspage(request, page):
    themes = Theme.objects.all()
    context={
        'page': page,
        'themes': themes,
    }
    return render (request, 'authentication/discussion.html', context)
