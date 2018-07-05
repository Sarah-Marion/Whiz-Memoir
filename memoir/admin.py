from django.contrib import admin
from .models import Entry, Task, Note, Event

# Register your models here.
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('description', 'author', 'date')


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('description', 'author', 'date')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('description', 'author', 'date')