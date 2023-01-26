from django.contrib import admin

# Register your models here.

from .models import Note

class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'content')


admin.site.register(Note, NoteAdmin)
