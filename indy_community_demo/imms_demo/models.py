from django.db import models

from indy_community.models import *


# base class for Immunizations conversations - reference to each involved Conversation
# these are for the involved organization (School or Immunization Repository)
class ImmunizationConversation(models.Model):
    wallet = models.ForeignKey(IndyWallet, to_field="wallet_name", on_delete=models.CASCADE)
    wallet_role = models.ForeignKey(IndyOrgRole, blank = True, null=True, on_delete=models.CASCADE)
    # for a school - this is a referece to the consent credential sent to the parent
    consent_enablement = models.ForeignKey(AgentConversation, related_name='consent_enablement', on_delete=models.CASCADE)
    # a reference to the proof request between the school and repo (for both orgs)
    imms_status_proof = models.ForeignKey(AgentConversation, related_name='imms_status_proof', on_delete=models.CASCADE)
    # for the repo - a reference to the consent proof from the parent
    imms_consent_proof = models.ForeignKey(AgentConversation, related_name='imms_consent_proof', on_delete=models.CASCADE)
    status = models.CharField(max_length=20)

    def __str__(self):
        return self.wallet.wallet_name + ' ' + self.wallet_role + ' ' + self.status

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
