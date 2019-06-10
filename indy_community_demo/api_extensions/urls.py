from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.views.generic import TemplateView
from django.conf.urls import url
from .views import *

urlpatterns = [
    path('wallet/', get_wallet, name='wallet'),
    path('conn/', connect, name='conn'),
    path('list_conn/', list_connections, name='list_conn'),
    path('list_usr/', list_users, name='list_usr'),
    path('list_org/', list_orgs, name='list_org')
]