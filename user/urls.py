from django.conf.urls import url
from django.contrib import admin

from user.views import user_login
from . import views

urlpatterns = [
    url(r'^login/$', user_login, name='login'),
]