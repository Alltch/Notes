from django.contrib import admin
from .models import Note, Friend

admin.register(Note)(admin.ModelAdmin)
admin.register(Friend)(admin.ModelAdmin)

# Register your models here.
