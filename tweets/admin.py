from django.contrib import admin
from django.apps import apps
# Register your models here.
admin.site.register(apps.get_model('tweets', 'Tweet'))
