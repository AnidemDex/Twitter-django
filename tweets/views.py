from django.shortcuts import render
from django.utils import timezone
from django.apps import apps

Tweet = apps.get_model('tweets', 'Tweet')


def tweet_list():
    tweets = Tweet.objects.filter(
        created_at__lte=timezone.now()).order_by('created_at')
    return tweets
