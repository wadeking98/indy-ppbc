from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings

from .forms import *
from .views import *


urlpatterns = [
    path('', auth_views.LoginView.as_view(), name='login'),
]

