from django.urls import path
from .views import register, login, welcome, logout, user

urlpatterns = [
    path('', welcome),
    path('register', register),
    path('login', login),
    path('logout', logout),
    path('<user_name>', user)
]
