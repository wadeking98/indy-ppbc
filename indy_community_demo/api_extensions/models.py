from django.conf import settings
from django.db import models
from django.contrib.sessions.models import Session
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import Group, PermissionsMixin

from django.utils import timezone

from datetime import datetime, date, timedelta
import json

# Roles to which an organization can belong


class IndyWallet(models.Model):
    wallet_name = models.CharField(max_length=60, unique=True)
    wallet_config = models.TextField(max_length=4000, blank=True)

    def __str__(self):
        return self.wallet_name

# class IndyOrgRole(models.Model):
#     name = models.CharField(max_length=40, unique=True)

#     def __str__(self):
#         return self.name

# class IndyOrganization(models.Model):
#     org_name = models.CharField(max_length=60, unique=True)
#     wallet = models.ForeignKey(IndyWallet, to_field="wallet_name", related_name='wallet_org', blank = True, null=True, on_delete=models.CASCADE)
#     role = models.ForeignKey(IndyOrgRole, blank = True, null=True, on_delete=models.CASCADE)
#     ico_url = models.CharField(max_length=120, blank = True, null=True)
#     managed_wallet = models.BooleanField(default=True)

#     def __str__(self):
#         return self.org_name


# class AgentConnection(models.Model):
#     wallet = models.ForeignKey(IndyWallet, to_field="wallet_name", on_delete=models.CASCADE)
#     partner_name = models.CharField(max_length=60)
#     invitation = models.TextField(max_length=4000, blank=True)
#     token = models.CharField(max_length=80, blank=True)
#     status = models.CharField(max_length=20)
#     connection_type = models.CharField(max_length=20)
#     connection_data = models.TextField(max_length=4000, blank=True)

#     def __str__(self):
#         return  ":" + self.partner_name + ", " +  self.status
