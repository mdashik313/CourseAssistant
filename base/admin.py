from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(University)
admin.site.register(Department)
admin.site.register(Content)
admin.site.register(Comment)
admin.site.register(Reaction)
admin.site.register(Notification)
admin.site.register(Unread_Counts)
admin.site.register(What_if)
