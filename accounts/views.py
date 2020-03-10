from django.shortcuts import render, redirect
from django.contrib.auth import logout as close_session
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as start_session
from django.contrib.auth.forms import UserCreationForm
from tweets.views import tweet_list
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from .models import UserProfile
from tweets.forms import TweetForm
from tweets.models import Tweet
from tweets.views import get_new_tweetform


def welcome(request):
    if request.user.is_authenticated:
        form = get_new_tweetform(request)

        context = {'tweets': tweet_list(), 'form': form}
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
    form = get_new_tweetform(request)
    try:
        user_id = User.objects.get(username=user_name).id
        user_db = UserProfile.objects.get(user=user_id)
        user_tweets = Tweet.objects.filter(author=user_id)
    except ObjectDoesNotExist:
        user_db = 'Este usuario no existe'
        user_tweets = ''

    contexto = {'user': user_db, 'tweets': user_tweets, 'form': form}
    return render(request, "accounts/user_profile.html", context=contexto)


def edit_user(request):
    contexto = {}
    return render(request, "accounts/edit_user.html", context=contexto)
