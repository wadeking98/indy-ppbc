from django.http import HttpResponseBadRequest, HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, get_user_model, login
# from django.urls import reverse
# from django.conf import settings
from indy_community.agent_utils import *
from indy_community.models import *
from indy_community.forms import *

from pprint import pprint
import json

def get_wallet(request):
    wallet_name = request.session['wallet_name']

    # validate it is the correct wallet
    wallet_type = request.session['wallet_type']
    wallet_owner = request.session['wallet_owner']
    if wallet_type == 'user':
        # verify current user owns wallet
        if wallet_owner == request.user.email:
            return JsonResponse({'wallet':wallet_name}) 
        raise Exception('Error wallet/session config is not valid')
    elif wallet_type == 'org':
        # verify current user has relationship to org that owns wallet
        for org in request.user.indyrelationship_set.all():
            if org.org.org_name == wallet_owner:
                return JsonResponse({'wallet':wallet_name})
        raise Exception('Error wallet/session config is not valid')
    else:
        raise Exception('Error wallet/session config is not valid')


def wallet_for_current_session(request):
    """
    Determine the current active wallet
    """

    wallet_name = request.session['wallet_name']
    wallet = get_user_model().objects.filter(wallet=wallet_name).first()

    # validate it is the correct wallet
    wallet_type = request.session['wallet_type']
    wallet_owner = request.session['wallet_owner']
    if wallet_type == 'user':
        # verify current user owns wallet
        if wallet_owner == request.user.email:
            return wallet
        raise Exception('Error wallet/session config is not valid')
    elif wallet_type == 'org':
        # verify current user has relationship to org that owns wallet
        for org in request.user.indyrelationship_set.all():
            if org.org.org_name == wallet_owner:
                return wallet
        raise Exception('Error wallet/session config is not valid')
    else:
        raise Exception('Error wallet/session config is not valid')


def connect(request, form_template='indy/connection/request.html'):
    form = SendConnectionInvitationForm(request.POST)
    if request.method=='POST':
        if not form.is_valid():
            #return render(request, 'indy/form_response.html', {'msg': 'Form error', 'msg_txt': str(form.errors)})
            return HttpResponse("form invalid")
        else:
            cd = form.cleaned_data
            #the email of the partenr we're trying to connect to
            partner_name = cd.get('partner_name')

            #this user's wallet name
            wallet_name = cd.get('wallet_name')
            #double check this user's wallet
            wallet_name_check = request.session['wallet_name']
            assert(wallet_name == wallet_name_check)

            

            # this user's email
            this_name = get_user_model().objects.filter(wallet=wallet_name).first().email
            this_wallet = wallet_for_current_session(request).wallet
            partner_wallet = get_user_model().objects.filter(email=partner_name).first().wallet
            test = get_user_model().objects.filter(email=partner_name).all()
           
            # send connection invitation from partner to this client
            print(test)
            my_connection = send_connection_invitation(this_wallet, partner_name)
            their_connection = AgentConnection(
                wallet = partner_wallet,
                partner_name = partner_name,
                invitation = my_connection.invitation,
                token = my_connection.token,
                connection_type = 'Inbound',
                status = 'Pending')
            their_connection.save()
            #outbound = send_connection_confirmation(wallet_for_current_session(request).wallet, inbound.connection_id, partner_name, None)
            return HttpResponse(my_connection.connection_data)
            # set wallet password
            # TODO vcx_config['something'] = raw_password

            # build the connection and get the invitation data back
    else:
        return HttpResponse("hello");            

