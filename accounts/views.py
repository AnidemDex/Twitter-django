from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout as close_session
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as start_session
from django.contrib.auth.forms import UserCreationForm
from tweets.views import tweet_list
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

from .models import UserProfile
from .forms import UserEditForm
from tweets.forms import TweetForm
from tweets.models import Tweet
from tweets.views import get_new_tweetform


@login_required(login_url='/login', redirect_field_name='')
def welcome(request):
    new_tweet_form = get_new_tweetform(request)
    user_db = UserProfile.objects.all()
    context = {'tweets': tweet_list(), 'form': new_tweet_form,
               'users': user_db}
    return render(request, "welcome.html", context=context)


def register(request):
    if request.user.is_authenticated:
        return redirect('/')

    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(data=request.POST)
        if form.is_valid():

            user = form.save()
            user.refresh_from_db()

            if user is not None:
                start_session(request, user)
                return redirect('accounts/edit_user.html')

    return render(request, "accounts/register.html", {'form': form})


def login(request):
    if request.user.is_authenticated:
        return redirect('/')

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
        user_db = get_object_or_404(User.objects.get(username=user_name))
        user_tweets = ''

    contexto = {'user': user_db, 'tweets': user_tweets, 'form': form}
    return render(request, "accounts/user_profile.html", context=contexto)


@login_required(login_url='/login', redirect_field_name='')
def edit_user(request, user_name):
    user = User.objects.get(username=user_name).id
    user = UserProfile.objects.get(user=user)
    form = UserEditForm()
    if request.method == "POST":
        form = UserEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
    contexto = {'form': form, }
    return render(request, "accounts/edit_user.html", context=contexto)
