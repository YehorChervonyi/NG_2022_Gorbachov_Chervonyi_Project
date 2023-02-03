from django.db import models

# Create your models here.
from django.contrib.auth.models import User
User._meta.get_field('email')._unique = True




class Theme(models.Model):
    name_theme = models.CharField(max_length=100)

    def __str__(self):
        return self.name_theme


class Discussion(models.Model):
    name_discussion = models.CharField(max_length=100)
    description = models.TextField(max_length=2048,null=True, blank=True)
    theme = models.ForeignKey(Theme, blank=True, null=True, on_delete=models.CASCADE,)
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)
    host = User.username

    def __str__(self):
        return self.name_discussion
