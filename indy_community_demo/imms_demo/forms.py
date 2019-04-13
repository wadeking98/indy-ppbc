from django import forms
from django.contrib.auth import get_user_model

import json

# tbd once we have models
#from .models import *


###############################################################
# Forms to support immunizations consent/presentation workflow
###############################################################
class IssueHealthIdAndImmsStatusForm(forms.Form):
    connection_id = forms.CharField(widget=forms.HiddenInput())
    first_name = forms.CharField(label='First Name', max_length=60)
    last_name = forms.CharField(label='Last Name', max_length=80)
    birth_date = forms.DateField()
    health_id = forms.CharField(label='Health ID', max_length=20)
    health_id_type = forms.ChoiceField(label='Health ID Type', 
                                       choices=[('Adult', 'Adult'), ('Child', 'Child')],
                                       help_text='"Adult" or "Child".')
    health_id_parent = forms.CharField(label='Parent Health ID (if Child ID Type)', max_length=20,
                                       required=False,
                                       help_text='Optional, required if Health ID Type is "Child".')
    issue_date = forms.DateField()
    immunization_status = forms.ChoiceField(label='Immunization Status', 
                                       choices=[('OK', 'OK'), ('Not OK', 'Not OK'), ('Unknown', 'Unknown')],
                                       help_text='"OK" or "Not OK".')
    immunization_status_date = forms.DateField()

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


class ImmsStatusProofRequestForm(forms.Form):
    """
    Step 2 - The school issues a consent enablement credential to the parent, simultaneously
             sending a proof request to the imms repo to get the child's immunization status
    """
    first_name_parent = forms.CharField(label='First Name (Parent)', max_length=60)
    last_name_parent = forms.CharField(label='Last Name (Parent)', max_length=80)
    health_id_parent = forms.CharField(label='Last Name (Parent)', max_length=20)
    first_name_child = forms.CharField(label='First Name (Child)', max_length=60)
    last_name_child = forms.CharField(label='Last Name (Child)', max_length=80)
    health_id_child = forms.CharField(label='Last Name (Parent)', max_length=20)
    school_did = forms.CharField(label='DID (School)', max_length=60)

    def __init__(self, *args, **kwargs):
        super(ImmsStatusProofRequestForm, self).__init__(*args, **kwargs)
        self.fields['first_name_parent'].widget.attrs['readonly'] = True
        self.fields['last_name_parent'].widget.attrs['readonly'] = True
        self.fields['health_id_parent'].widget.attrs['readonly'] = True
        self.fields['first_name_child'].widget.attrs['readonly'] = True
        self.fields['last_name_child'].widget.attrs['readonly'] = True
        self.fields['health_id_child'].widget.attrs['readonly'] = True
        self.fields['school_did'].widget.attrs['readonly'] = True


class ImmsRequestProofRequestForm(ImmsStatusProofRequestForm):
    """
    Step 3 - The imms repo receives the proof request from the school, and sends a proof request 
             to the parent to verify consent
    """

    def __init__(self, *args, **kwargs):
        super(ImmsRequestProofRequestForm, self).__init__(*args, **kwargs)


class ImmsStatusProofResponseForm(ImmsRequestProofRequestForm):
    """
    Step 4 - Upon receipt of the consent proof from the parent, issue the immunization status 
             proof to the school
    """
    immunizaton_status = forms.CharField(label='Immunization Status', max_length=20)

    def __init__(self, *args, **kwargs):
        super(ImmsStatusProofResponseForm, self).__init__(*args, **kwargs)
        self.fields['immunizaton_status'].widget.attrs['readonly'] = True

