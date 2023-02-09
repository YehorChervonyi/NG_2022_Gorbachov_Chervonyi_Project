from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from . forms import RegisterUserForm, User, ThemeForm, DiscussionForm, CommentsForm
from . models import Theme, Discussion, Comments, Notification
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator


# Create your views here.
def home_page(request):
    page = "Home"
    themes = Theme.objects.all()
    discussions_all = Discussion.objects.all().order_by('id')
    pag = Paginator(discussions_all.reverse(), 5)
    pg = request.GET.get('pg')
    discussions = pag.get_page(pg)
    context = {
        'discussions': discussions,
        'themes': themes,
        'page': page,
    }
    return render(request, 'authentication/main.html', context)

# This function logging user to his account.
def login_user(request):
    themes = Theme.objects.all()
    if request.method == "POST":
        email = request.POST['email'].strip()
        password = request.POST['password'].strip()
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
        'themes': themes
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

@login_required(login_url='login')
@permission_required('admin', raise_exception=True)
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
        elif form.errors:
            messages.warning(request, 'Theme cant include +-/%?#$*^@!&[]')
        else:
            messages.warning(request, "Theme with this name already exist")
        themes = Theme.objects.all()
    context = {'form': form,
               'themes': themes}
    return render(request, 'authentication/createtheme.html', context)

@login_required(login_url='login')
def create_discussion(request):
    themes = Theme.objects.all()
    form = DiscussionForm
    current_user = request.user.username
    if request.method == "POST":
        form = DiscussionForm(request.POST, request.FILES)
        if form.is_valid():
            discussion = form.save(commit=False)
            discussion.author_discussion = current_user
            discussion.save()
            messages.success(request, "Discussion created. We believe you wil enjoy")
            return redirect('home')
    context = {'form': form,
               'themes': themes,
               }
    return render(request, 'authentication/creatediscussion.html', context)

def themepage(request, page):
    themes = Theme.objects.all()
    discussions = None
    for one_theme in themes:
        if str(one_theme) == str(page):
            discussions_all = Discussion.objects.filter(theme=one_theme).order_by('create_time')
            pag = Paginator(discussions_all.reverse(), 5)
            pg = request.GET.get('pg')
            discussions = pag.get_page(pg)
    context = {
        'page': page,
        'themes': themes,
        'discussions': discussions,
    }

    return render(request, 'authentication/theme.html', context)


def discussionpage(request, page, discussionid):
    themes = Theme.objects.all()
    form = CommentsForm
    current_user = request.user
    print(current_user)
    discussions = Discussion.objects.all()
    discusss = None
    comments = None
    for onediscussion in discussions:
        if str(onediscussion.id) == str(discussionid):
            discusss = Discussion.objects.filter(id=onediscussion.id)
            comments = Comments.objects.filter(discussion=onediscussion)
            if request.method == "POST":

                form = CommentsForm(request.POST)
                if form.is_valid():
                    comment = form.save(commit=False)
                    comment.author_comment = current_user
                    comment.discussion = Discussion.objects.filter(id=onediscussion.id)[0]

                    lst = (', ', ' ', ',', '.', '. ', '!', '! ',
                            '?', '? ', ') ', ')', '( ', '(')
                    text = comment.text_comment
                    for word in text.split():
                        for char in lst:
                            if char in word[0]:
                                break
                            word = word.split(char)[0]
                        if word[0] == "@":
                            user = word[1:]

                            try:
                                userdb = User.objects.get(username=user)
                                Notification.objects.create(owner=userdb,
                                                            notification="You was mentioned in discussion",
                                                            url="/"+page+"/"+discussionid)
                            except:
                                messages.warning(request, "User doesnt exist, write correct username")
                                break


                    comment.save()
                    messages.success(request, "Thank you for comment")
                    return HttpResponseRedirect('/'+page+'/'+discussionid)

    context = {
        'page': page,
        'form': form,
        'themes': themes,
        'discussionid': discussionid,
        'discusss': discusss,
        'comments': comments
    }
    return render(request, 'authentication/discussion.html', context)

@login_required(login_url='login')
def notificationspage(request):
    themes = Theme.objects.all()
    current_user = request.user
    notifications_all = Notification.objects.filter(owner=current_user).order_by('create_time')
    pag = Paginator(notifications_all.reverse(), 5)
    pg = request.GET.get('pg')
    notifications = pag.get_page(pg)
    page = "Notifications"
    context = {
        'themes': themes,
        'notifications': notifications,
        'page': page,
    }
    return render(request, 'authentication/notifications.html', context)
