from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import Theme, Discussion, Comments


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'firstname'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'lastname'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder':'email'}))

    def __str__(self):
        return User.username
    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['username'].help_text="Username required. 50 characters or fewer. Letters, digits and @/./+/-/_ only."
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password1'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Password2'
        self.fields['password2'].help_text = ''


class ThemeForm(ModelForm):
    class Meta:
        model = Theme
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(ThemeForm, self).__init__(*args, **kwargs)

        self.fields['name_theme'].widget.attrs['class'] = 'form-control'
        self.fields['name_theme'].widget.attrs['placeholder'] = 'Name Theme'

class DiscussionForm(ModelForm):
    class Meta:
        model = Discussion
        fields = ('name_discussion', 'description', 'theme', 'file')
    def __init__(self, *args, **kwargs):
        super(DiscussionForm, self).__init__(*args, **kwargs)

        self.fields['name_discussion'].widget.attrs['class'] = 'form-control'
        self.fields['name_discussion'].widget.attrs['placeholder'] = 'Name Discussion'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['placeholder'] = 'Description'
        self.fields['description'].widget.attrs['style'] = 'resize:none'
        self.fields['description'].widget.attrs['cols'] = '20'
        self.fields['description'].widget.attrs['rows'] = '10'
        self.fields['theme'].widget.attrs['class'] = 'form-control'
        self.fields['theme'].widget.attrs['placeholder'] = 'Theme'
        self.fields['file'].widget.attrs['class'] = 'form-control'
        self.fields['file'].widget.attrs['type'] = 'file'

class CommentsForm(ModelForm):
    class Meta:
        model = Comments
        fields = ('text_comment',)
    def __init__(self, *args, **kwargs):
        super(CommentsForm, self).__init__(*args, **kwargs)

        self.fields['text_comment'].widget.attrs['class'] = 'form-control'
        self.fields['text_comment'].widget.attrs['placeholder'] = 'Your comment here...'
        self.fields['text_comment'].widget.attrs['rows'] = '10'

