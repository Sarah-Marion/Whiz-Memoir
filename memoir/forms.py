from django import forms
# from .models import Hood, Profile, Business, Post, Social_Amenities
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms.widgets import TextInput, PasswordInput
from .models import *

class SignUpForm(UserCreationForm):
    """
    Class that creates a Sign up form
    """
    email = forms.EmailField(max_length=250)

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = ' Username'
        self.fields['email'].widget.attrs['placeholder'] = ' Email'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm your Password'

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        unique_together = ('email')

class LoginForm(AuthenticationForm):
    """
    class that creates a Login form
    """
    username = forms.CharField(widget=TextInput(attrs={'class':'validate', 'placeholder':'Username'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder':'Password'}))



TASK = "task"
NOTE = "note"
EVENT = "event"

ENTRY_CHOICES = (
    (None, ""),
    (TASK, 'Task'),
    (NOTE, 'Note'),
    (EVENT, 'Event'),
)


class EntryCreationForm(forms.Form):
    type = forms.ChoiceField(label="Type", choices=ENTRY_CHOICES, error_messages={'required': 'Kindly select the type of event'})
    entry = forms.CharField(label="Entry", error_messages={'required': 'Kindly input some text for your entry'})
    date = forms.DateField(label="Date", error_messages={'required': 'Kindly pick an entry date '})
    priority = forms.BooleanField(label="Precedence", required=False)
    explore = forms.BooleanField(label="Explore", required=False)
    inspiration = forms.BooleanField(label="Motivation", required=False)

    def save(self, user):
        if self.is_valid():
            if self.cleaned_data['type'] == TASK:
                model = Task()
            elif self.cleaned_data['type'] == NOTE:
                model = Note()
                model.explore = self.cleaned_data['explore']
                model.inspiration = self.cleaned_data['inspiration']
            elif self.cleaned_data['type'] == EVENT:
                model = Event()

            model.date = self.cleaned_data['date']
            model.description = self.cleaned_data['entry']
            model.priority = self.cleaned_data['priority']
            model.author = user

            model.save() 