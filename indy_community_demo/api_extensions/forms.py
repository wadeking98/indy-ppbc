
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.db.models import Q

import json

class WalletNameForm(forms.Form):
    wallet_name = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(WalletNameForm, self).__init__(*args, **kwargs)
        self.fields['wallet_name'].widget.attrs['readonly'] = True


class SendConnectionInvitationForm(WalletNameForm):
    partner_name = forms.CharField(label='Partner Name', max_length=60)

    def __init__(self, *args, **kwargs):
        super(SendConnectionInvitationForm, self).__init__(*args, **kwargs)
        self.fields['wallet_name'].widget.attrs['readonly'] = True
        self.fields['wallet_name'].widget.attrs['hidden'] = True