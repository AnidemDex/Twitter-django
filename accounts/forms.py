from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.apps import apps

Tweet = apps.get_model('tweets', 'forms')


class UserProfileForm(UserCreationForm):
    class Meta:
        model = UserProfile
        fields = ['user', 'password1', 'password2']
