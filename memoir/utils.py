from .models import Entry, Task, Event, Note

def get_all_entries(user, date = None):
    """
    Gets all entries for a specified date and user. 
    If date is removed, it will retrieve all entries.

    :param user: The user whose entries should be retrieved
    :param date: The date to retrieve entries from
    :return: A list of all entries for the user
    """
    if date:
        tasks = list(Task.objects.filter(author = user, date = date))
        events = list(Event.objects.filter(author = user, date = date))
        notes = list(Note.objects.filter(author = user, date = date))
    else:
        tasks = list(Task.objects.filter(author = user))
        events = list(Event.objects.filter(author = user))
        notes = list(Note.objects.filter(author = user))

    entries = tasks + events + notes
    return sorted(entries, key=lambda entry: entry.date_created)

