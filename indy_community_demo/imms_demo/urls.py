from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings

from .forms import *
from .views import *


urlpatterns = [
    path('ha_issue_credentials/', ha_issue_credentials, name='ha_issue_credentials'),
    path('school_request_health_id/', school_request_health_id, name='school_request_health_id'),
    path('', auth_views.LoginView.as_view(), name='login'),
]

