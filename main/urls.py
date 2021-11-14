
from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', home , name="home"),
    path('register', register , name="register"),
    path('login', logindef, name="login"),
    path('token', token, name="token"),
    path('success', success, name="success"),
    path('verify/<token>' , verify , name="verify"),

]
