from django.shortcuts import render, redirect
from django.contrib.auth import logout as close_session
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as start_session
from django.contrib.auth.forms import UserCreationForm
from tweets.views import tweet_list
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


def welcome(request):
    if request.user.is_authenticated:
        context = {'tweets': tweet_list()}
        return render(request, "welcome.html", context=context)
    else:
        return redirect('/login')


def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(data=request.POST)
        if form.is_valid():

            user = form.save()
            user.refresh_from_db()

            if user is not None:
                start_session(request, user)
                return redirect('/')

    return render(request, "accounts/register.html", {'form': form})


def login(request):
    form = AuthenticationForm()

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                start_session(request, user)
                return redirect('/')
    return render(request, "accounts/login.html", {'form': form})


def logout(request):
    close_session(request)
    return redirect('/')


def user(request, user_name):
    try:
        user_db = User.objects.get(username=user_name)
    except ObjectDoesNotExist:
        user_db = 'Este usuario no existe'
    return render(request, "accounts/user_profile.html", {'user': user_db})
