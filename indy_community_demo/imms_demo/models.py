from django.db import models
from datetime import datetime, date, timedelta

from indy_community.models import *


# base class for Immunizations conversations - reference to each involved Conversation
# these are for the involved organization (School or Immunization Repository)
class SchoolImmunizationConversation(models.Model):
    wallet = models.ForeignKey(IndyWallet, to_field="wallet_name", on_delete=models.CASCADE)
    wallet_role = models.ForeignKey(IndyOrgRole, blank = True, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=80)
    first_name_parent = models.CharField(max_length=60)
    last_name_parent = models.CharField(max_length=80)
    # for a school - this is a referece to the health id proof request sent to the parent
    health_id_request = models.ForeignKey(AgentConversation, related_name='health_id_request', blank = True, null=True, on_delete=models.CASCADE)
    # for a school - this is a referece to the consent credential sent to the parent
    consent_enablement_offer = models.ForeignKey(AgentConversation, related_name='consent_enablement_offer', blank = True, null=True, on_delete=models.CASCADE)
    # a reference to the proof request between the school and repo (for both orgs)
    imms_status_request = models.ForeignKey(AgentConversation, related_name='imms_status_request', blank = True, null=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    msg = models.CharField(max_length=200, blank = True, null=True)
    initiation_date = models.DateField()

    def __str__(self):
        return self.wallet.wallet_name + ' ' + self.wallet_role + ' ' + self.status

class RepoImmunizationConversation(models.Model):
    wallet = models.ForeignKey(IndyWallet, to_field="wallet_name", on_delete=models.CASCADE)
    wallet_role = models.ForeignKey(IndyOrgRole, blank = True, null=True, on_delete=models.CASCADE)
    health_id = models.CharField(max_length=20, blank = True, null=True)
    consenting_health_id = models.CharField(max_length=20, blank = True, null=True)
    # a reference to the proof request between the school and repo (for both orgs)
    imms_status_proof = models.ForeignKey(AgentConversation, related_name='imms_status_proof', blank = True, null=True, on_delete=models.CASCADE)
    # a reference to the consent proof request between the repo and parent
    imms_consent_proof = models.ForeignKey(AgentConversation, related_name='imms_consent_proof', blank = True, null=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    msg = models.CharField(max_length=200, blank = True, null=True)
    initiation_date = models.DateField()

    def __str__(self):
        return self.wallet.wallet_name + ' ' + self.wallet_role + ' ' + self.status

# to keep track of the parent's consent-related conversations
class UserImmunizationConversation(models.Model):
    wallet = models.ForeignKey(IndyWallet, to_field="wallet_name", on_delete=models.CASCADE)
    proof_id = models.CharField(max_length=60)
    first_name = models.CharField(max_length=60, blank = True, null=True)
    last_name = models.CharField(max_length=80, blank = True, null=True)
    first_name_parent = models.CharField(max_length=60, blank = True, null=True)
    last_name_parent = models.CharField(max_length=80, blank = True, null=True)
    # parent - this is a referece to the health id proof request sent to the parent
    health_id_proof = models.ForeignKey(AgentConversation, related_name='health_id_proof', blank = True, null=True, on_delete=models.CASCADE)
    # parent - this is a referece to the consent credential sent to the parent
    consent_enablement = models.ForeignKey(AgentConversation, related_name='consent_enablement', blank = True, null=True, on_delete=models.CASCADE)
    # a reference to the proof request between the school and repo (for both orgs)
    imms_consent_request = models.ForeignKey(AgentConversation, related_name='imms_consent_request', blank = True, null=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    msg = models.CharField(max_length=200, blank = True, null=True)
    initiation_date = models.DateField()

    def __str__(self):
        return self.wallet.wallet_name + ' ' + 'User' + ' ' + self.status


# track health identities issued by the HA (ref to wallet)
class HealthIdentity(models.Model):
    issuer = models.ForeignKey(IndyWallet, to_field="wallet_name", on_delete=models.CASCADE)
    health_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=120)
    birth_date = models.DateField()
    health_id_type = models.CharField(max_length=20)
    parent_health_id = models.CharField(max_length=20, blank = True, null=True)
    issue_date = models.DateField()
    last_issued = models.ForeignKey(AgentConversation, related_name='health_id_issued', blank = True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.health_id + ': ' + self.first_name + ' ' + self.last_name


# track issued immunizatons status
class ImmunizationStatusCertificate(models.Model):
    issuer = models.ForeignKey(IndyWallet, to_field="wallet_name", on_delete=models.CASCADE)
    health_id = models.ForeignKey(HealthIdentity, to_field="health_id", related_name='imms_status_certificate', on_delete=models.CASCADE)
    immunization_status = models.CharField(max_length=20)
    immunization_status_date = models.DateField()
    issue_date = models.DateField()
    last_issued = models.ForeignKey(AgentConversation, related_name='imms_status_issued', blank = True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.health_id.health_id + ': ' + self.health_id.first_name + ' ' + self.health_id.last_name
