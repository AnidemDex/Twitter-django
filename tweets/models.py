from django.db import models
from django.contrib.auth.models import User
from accounts.models import UserProfile
from django.utils import timezone
# Create your models here.


class Tweet(models.Model):
    created_at = models.DateField(auto_now_add=True)
    author = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE)
    text = models.CharField(max_length=160)

    def publish(self):
        self.save()

    def __str__(self):
        return f'Tweet de @{self.author}'
