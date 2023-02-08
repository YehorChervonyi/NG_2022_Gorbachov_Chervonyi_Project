from django.contrib import admin
from .models import Discussion, Theme, Comments, Notification


admin.site.register(Discussion)
admin.site.register(Theme)
admin.site.register(Comments)
admin.site.register(Notification)

