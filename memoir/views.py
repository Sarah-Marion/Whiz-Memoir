from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from .forms import SignUpForm, LoginForm, EntryCreationForm
from .models import Task
from .utils import get_all_entries
from dates.utils import get_dates, get_months_until_today, get_next_seven_days
from django.core.urlresolvers import reverse
from collections import defaultdict
from django.http import HttpResponse, Http404,    HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import date
from django.contrib.auth.models import User
from django.contrib.auth import login
# import json
# import request
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core import serializers
from django.utils import six


# Create your views here.
def index(request):
    return render(request, 'index.html')
    
def signup(request):
    """
    View function that ensures a user is first authenticated prior using/accesing the application.
    """
    current_user = request.user
    if current_user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your Whiz Memoir Account'
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def account_activation_sent(request):
    """
    View function that sends out an activation email to a user
    """
    current_user = request.user
    if current_user.is_authenticated():
        return HttpResponseRedirect('/')
    return render(request, 'registration/activation_complete.html')


def activate(request, uidb64, token):
    """
    View funtion that activates their account once they signup to use the application
    """
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        # user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('logout')
    else:
        return render(request, 'registration/account_activation_invalid.html')



def create_entry(request):
    """
    View function that lets a user create an entry
    """
    if request.method == 'POST':
        form = EntryCreationForm(request.POST)

        if form.is_valid():
            form.save(request.user)
            messages.success(request, "Your Input was Successfully added")

            # Returns a user to where they were
            return HttpResponseRedirect(request.POST['next'])
        else:
            # Retains user on current page
            return render(request, 'memoirs.html', {
                "form" : form,
                "next" : request.POST['next'],
                "entries" : request.session.get('entries'),
            })
    else:
        # If a GET request is made, redirect back home
        return HttpResponseRedirect(reverse("home"))



def view_all_entries(request, future_only=False):
    """
    View function that lets a user view all entries
    """

    entries = get_all_entries(request.user)

    entry_dict = defaultdict(list)

    for entry in entries:
        if future_only and (entry.date < date.today()):
            continue
        entry_dict[entry.date].append(entry)

    entries = sorted(entry_dict.items())
    request.session['entries'] = entries
    return render(request, 'memoirs.html', {"entries": entries,})


def view_next_seven_days_entries(request):
    """
    View function that lets a user view their entries for the next seven days
    """
    user = request.user
    entries = {}

    for day in get_next_seven_days():
        entries[day] = get_all_entries(user, day)
    entries = sorted(entries.items())
    request.session['entries'] = entries
    return render(request, 'memoirs.html', {"entries": entries})


def view_month_entries(request, month=date.today().month, year=date.today().year):
    """
    View function that lets a user view month entries
    """
    user = request.user
    entries = {}
    month = int(month)
    year = int(year)

    for day in get_dates(month, year):
        entries[day] = get_all_entries(user, day)
    entries = sorted(entries.items())
    request.session['entries'] = entries
    return render(request, 'memoirs.html', {"entries": entries,})


def toggle_todo(request, todo_id):
    task = get_object_or_404(klass = Task, pk=todo_id)
    task.completed = not task.completed
    task.save()
    return HttpResponse("Successfully updated {0}".format(task.description))

def view_chronicles(request):
    months_years = get_months_until_today(request.user.date_joined.month, request.user.date_joined.year)
    months = []

    for month_year in months_years:
        month = date(month_year[1], month_year[0], 1)
        months.append(month)
    return render(request, 'chronicles.html', {"months": months,})