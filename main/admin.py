from django.contrib import admin
from .models import Note, CustomUser, FriendRequest, Friend

admin.site.register(Note)
admin.site.register(FriendRequest)
admin.site.register(Friend)
admin.site.register(CustomUser)
# Register your models here.
