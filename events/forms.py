from django import forms
from django.contrib.auth.models import User
from .models import Event, TicketsHolder#, UserProfile,

class UserSignup(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email' ,'password']

        widgets={
        'password': forms.PasswordInput(),
        }


class UserLogin(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ["event_organizer"]

class TicketForm(forms.ModelForm):
    class Meta:
        model = TicketsHolder
        fields = ['tickets']


# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = ('bio', 'location', 'birth_date')
