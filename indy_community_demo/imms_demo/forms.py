from django import forms
from django.contrib.auth import get_user_model

import json

# tbd once we have models
#from .models import *


###############################################################
# Forms to support immunizations consent/presentation workflow
###############################################################
class HealthIdsProofRequestForm(forms.Form):
    """
    Step 1 - The school has to issue a proof request to get the health id's for the parent and child
    """
    first_name_parent = forms.CharField(label='First Name (Parent)', max_length=60)
    last_name_parent = forms.CharField(label='Last Name (Parent)', max_length=80)
    first_name_child = forms.CharField(label='First Name (Child)', max_length=60)
    last_name_child = forms.CharField(label='Last Name (Child)', max_length=80)

    def __init__(self, *args, **kwargs):
        super(HealthIdsProofRequestForm, self).__init__(*args, **kwargs)
        #self.fields['wallet_name'].widget.attrs['readonly'] = True


class ImmsStatusProofRequestForm(forms.Form):
    """
    Step 2 - The school issues a consent enablement credential to the parent, simultaneously
             sending a proof request to the imms repo to get the child's immunization status
    """

    def __init__(self, *args, **kwargs):
        super(ImmsStatusProofRequestForm, self).__init__(*args, **kwargs)
        #self.fields['wallet_name'].widget.attrs['readonly'] = True


class ImmsRequestProofRequestForm(forms.Form):
    """
    Step 3 - The imms repo receives the proof request from the school, and sends a proof request 
             to the parent to verify consent
    """

    def __init__(self, *args, **kwargs):
        super(ImmsRequestProofRequestForm, self).__init__(*args, **kwargs)
        #self.fields['wallet_name'].widget.attrs['readonly'] = True


class ImmsStatusProofResponseForm(forms.Form):
    """
    Step 4 - Upon receipt of the consent proof from the parent, issue the immunization status 
             proof to the school
    """

    def __init__(self, *args, **kwargs):
        super(ImmsStatusProofResponseForm, self).__init__(*args, **kwargs)
        #self.fields['wallet_name'].widget.attrs['readonly'] = True

