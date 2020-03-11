from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django import forms
# Create your models here.


def upload_location(instance, filename):
    u = User.objects.get(id=instance.user_id)
    username = str(u.username)
    return f"{username}/{filename}"


class UserProfile(models.Model):
    user = models.OneToOneField(
        'auth.User', on_delete=models.CASCADE)
    nombres = models.CharField(max_length=60)
    apellidos = models.CharField(max_length=60)
    nacimiento = models.DateField(default='2000-01-01')
    description = models.CharField(max_length=160, blank=True)
    profile_picture = models.ImageField(
        upload_to='images/', default='images/Twitter_Logo_Blue.png')

    def __str__(self):
        return f"@{self.user.username}"


@receiver(post_save, sender=User)
def update_userprofile_signal(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
