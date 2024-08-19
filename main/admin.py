from django.contrib import admin
from .models import Note

admin.register(Note)(admin.ModelAdmin)

# Register your models here.
