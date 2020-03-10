from django.shortcuts import render
from django.utils import timezone
from django.apps import apps
from .forms import TweetForm

Tweet = apps.get_model('tweets', 'Tweet')


def tweet_list():
    tweets = Tweet.objects.filter(
        created_at__lte=timezone.now()).order_by('created_at')
    return tweets


def get_new_tweetform(request) -> TweetForm:
    form = None
    if request.user.is_authenticated:
        if request.method == "POST":
            form = TweetForm(data=request.POST)
            if form.is_valid():
                tweet = form.save(commit=False)
                tweet.author = request.user
                tweet.save()
        else:
            form = TweetForm()
    return form
