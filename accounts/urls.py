from django.urls import path
from .views import register, login, welcome, logout, user, edit_user

urlpatterns = [
    path('', welcome),
    path('register', register),
    path('login', login),
    path('logout', logout),
    path('<user_name>/edit', edit_user),
    path('<user_name>', user),
]
