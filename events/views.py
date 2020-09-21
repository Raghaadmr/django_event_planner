from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .forms import UserSignup, UserLogin , EventForm
from django.contrib import messages
from .models import Event

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
                return redirect('dashboard')
            messages.warning(request, "Wrong email/password combination. Please try again.")
            return redirect("login")
        messages.warning(request, form.errors)
        return redirect("login")


class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "You have successfully logged out.")
        return redirect("login")


def dashboard(request):
	events = Event.objects.all()
	context = {
		"events": events,
	}
	return render(request, 'dashboard.html', context)



def event_detail(request, classroom_id):
	event = Event.objects.get(id=event_id)
	context = {
		"event": event,
	}
	return render(request, 'event_detail.html', context)


def event_create(request):
	form = EventForm()
	if request.method == "POST":
		form = EventForm(request.POST, request.FILES or None)
		if form.is_valid():
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
	Event.objects.get(id=event_id).delete()
	messages.success(request, "Successfully Deleted!")
	return redirect('dashboard')
