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

