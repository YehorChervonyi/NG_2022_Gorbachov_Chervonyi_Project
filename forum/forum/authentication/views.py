from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model
from . token import account_activation_token
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
            user.is_active = False
            user.save()
            acc_activate_email(request, user, form.cleaned_data.get('email'))
            # messages.success(request, "Registration successful")
            return redirect('login')

    context = {
        'form': form,
        'themes':themes}
    return render(request, 'authentication/signup.html', context)

def acc_activate_email(request, user, emailto):
    mail_subject = 'Activate your user account.'
    message = render_to_string('authentication/accactivateemail.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[emailto])
    if email.send():
        messages.success(request, f"{user} check your email {emailto} inbox to confirm the registration")
    else:
        messages.warning(request, f'Problem sending confirmation email to {emailto}, check form fields.')

def activate(request, uidb64, token):
    user = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None:
        user.is_active = True
        user.save()
        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('login')
    else:
        messages.warning(request, 'Activation link is invalid!')
    return redirect('login')

def logout_user(request):
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
            messages.success(request, "Discussion created")
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
                    discusss.update(update_time=timezone.now())
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

def search(request):
    themes = Theme.objects.all()
    if request.method == "POST":
        searchfor = request.POST['searchfor']
        page = "Search | You search for: "+ searchfor
        discussions = Discussion.objects.filter(name_discussion__icontains=searchfor).order_by('create_time')
        context = {
            'discussions': discussions,
            'themes': themes,
            'page': page,
        }
        return render(request, 'authentication/search.html', context)
    else:
        page = "Wrong search"
        context = {
            'page': page,
        }
        return render(request, 'authentication/search.html', context)