from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

# Create your models here.
User._meta.get_field('email')._unique = True

class Theme(models.Model):
    name_theme = models.CharField(max_length=50, unique=True, validators=[RegexValidator('[+-/%?#$*^@!&[]]', inverse_match=True)])

    def __str__(self):
        return self.name_theme


class Discussion(models.Model):
    name_discussion = models.CharField(max_length=100)
    description = models.TextField(max_length=2048, null=True, blank=True)
    theme = models.ForeignKey(Theme, null=False, on_delete=models.CASCADE)
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)
    author_discussion = models.TextField(null=True)
    id = models.BigAutoField(primary_key=True)

    def __str__(self):
        return self.name_discussion


class Comments(models.Model):
    text_comment = models.TextField(max_length=1024)
    discussion = models.ForeignKey(Discussion, null=False, on_delete=models.CASCADE)
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)
    # author_comment = models.TextField(null=True)

    def __str__(self):
        return self.text_comment
