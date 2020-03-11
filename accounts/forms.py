from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.apps import apps
from django.forms import ModelForm


class UserProfileForm(UserCreationForm):
    class Meta:
        model = UserProfile
        fields = ['user', 'password1', 'password2']


class UserEditForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nombres', 'apellidos', 'nacimiento',
                  'description', 'profile_picture']
    pass
