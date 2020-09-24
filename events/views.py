from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .forms import UserSignup, UserLogin , EventForm, TicketForm #,ProfileForm
from django.contrib import messages
from .models import Event, TicketsHolder#, UserProfile
import datetime
from django.db.models import Q
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType

def home(request):
    return render(request, 'home.html')

class Signup(View):
    form_class = UserSignup
    template_name = 'signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            messages.success(request, "You have successfully signed up.")
            login(request, user)
            return redirect("home")
        messages.warning(request, form.errors)
        return redirect("signup")


class Login(View):
    form_class = UserLogin
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                messages.success(request, "Welcome Back!")
                return redirect("home")
            messages.warning(request, "Wrong email/password combination. Please try again.")
            return redirect("login")
        messages.warning(request, form.errors)
        return redirect("login")


class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "You have successfully logged out.")
        return redirect("login")

#User


def userdashboard(request):
    if not request.user.is_authenticated:
        return redirect("login")
    events = Event.objects.filter(event_organizer=request.user)
    context = {
        "events": events,
        "history": TicketsHolder.objects.filter(user=request.user, event__date__lt=datetime.datetime.now()),
        "reservations": TicketsHolder.objects.filter(user=request.user, event__date__gt=datetime.datetime.now()),
    }
    return render(request, "userdashboard.html", context)


def event_list(request):
    if not request.user.is_authenticated:
        return redirect("login")
    events = Event.objects.filter(date__gte=datetime.datetime.now())
    query = request.GET.get('search_term')
    if query:
        events = events.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(event_organizer__username__icontains=query)
        ).distinct()
    context = {
        "events": events
    }
    return render(request, 'event_list.html', context)



def book_ticket(request, event_id):
    if not request.user.is_authenticated:
        return redirect("login")
    form = TicketForm()
    event = Event.objects.get(id=event_id)
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            guest = form.save(commit=False)
            event.seats -= guest.tickets
            if guest.tickets < event.seats:
                guest.event = event
                guest.user=request.user
                event.save()
                guest.save()
                messages.success(request, "Successfully book the ticket/s")
            else:
                messages.warning(request, "Event is full!")

        return redirect("event-list")

    context = {
	"form": form,
	"event": event
	}
    return render(request, 'book_ticket.html', context)








# def profile(request, ):
#     user = User.objects.get(pk=user_id)
#     context = {
#     	"user": user,
#     }
#     return render(request, 'profile.html', context)



#Orignaizer

def dashboard(request):
    events = Event.objects.filter(event_organizer=request.user)
    context = {
        "events": events,
    }
    return render(request, 'dashboard.html', context)



def event_detail(request, event_id):
	event = Event.objects.get(id=event_id)
	users = TicketsHolder.objects.filter(event=event)
	context = {
		"event": event,
		"users":users,
	}
	return render(request, 'event_detail.html', context)

def event_create(request):
    if not request.user.is_authenticated:
        return redirect('login')
    form = EventForm()
    if request.method == "POST":
    	form = EventForm(request.POST, request.FILES or None)
    	if form.is_valid():
            event = form.save(commit=False)
            event.event_organizer = request.user
            form.save()
            messages.success(request, "Successfully Created!")
            return redirect('dashboard')
    	print (form.errors)
    context = {
        "form": form,
    }
    return render(request, 'event_create.html', context)


def event_update(request, event_id):
    event = Event.objects.get(id=event_id)
    if request.user ==event.event_organizer:
        form = EventForm(instance=event)
        if request.method == "POST":
        	form = EventForm(request.POST, request.FILES or None, instance=event)
        	if form.is_valid():
        		form.save()
        		messages.success(request, "Successfully Edited!")
        		return redirect('dashboard')
        	print (form.errors)
        context = {
        "form": form,
        "event": event,
        }
    return render(request, 'event_update.html', context)


def event_delete(request, event_id):
    if request.user ==event.event_organizer:
    	Event.objects.get(id=event_id).delete()
    	messages.success(request, "Successfully Deleted!")
    	return redirect('dashboard')
