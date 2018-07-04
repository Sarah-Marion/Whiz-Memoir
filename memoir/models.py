from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Entry(models.Model):
    """
    Entry class that defines objects of each Entry
    """
    date = models.DateField()
    date_created = models.DateField(auto_now_add=True)
    description = models.TextField()
    irrelevant = models.BooleanField(default = False)
    priority = models.BooleanField(default = False)
    author = models.ForeignKey(User)

    class Meta:
        # Abstract class that won't be created in the database
        abstract = True

    def __str__(self):
        return self.description

    # def save_entry(self):
    #     self.save()

    def get_class_name(self):
        return self.__class__.__name__


class Task(Entry):
    """
    Initialization of class task
    """
    completed = models.BooleanField(default = False)


class Note(Entry):
    """
    Initialization of class Note
    """
    inspiration = models.BooleanField(default = False)
    explore = models.BooleanField(default = False)

class Event(Entry):
    pass