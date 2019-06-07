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
    """ Returns the wallet of the current user in a json response
    predominantly used by front end to get this users wallet name

    Returns:
    JsonResponse: The wallet name of the current user
    """
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
    wallet_org = IndyOrganization.objects.filter(wallet=wallet_name).first()
    wallet_user = get_user_model().objects.filter(wallet=wallet_name).first()

    wallet = wallet_org if wallet_org is not None else wallet_user

    # validate it is the correct wallet
    wallet_type = request.session['wallet_type']
    wallet_owner = request.session['wallet_owner']
    if wallet_type == 'user':
        # verify current user owns wallet
        if wallet_owner == request.user.email:
            return wallet.wallet
        raise Exception('Error wallet/session config is not valid')
    elif wallet_type == 'org':
        # verify current user has relationship to org that owns wallet
        for org in request.user.indyrelationship_set.all():
            if org.org.org_name == wallet_owner:
                return wallet.wallet
        raise Exception('Error wallet/session config is not valid')
    else:
        raise Exception('Error wallet/session config is not valid')



def list_connections(
    request,
    ):
    """
    List Connections for the current wallet.
    """

    # expects a wallet to be opened in the current session
    wallet = wallet_for_current_session(request)
    connections = AgentConnection.objects.filter(wallet=wallet).all()

    ret_data = []
    for conn in connections:
        ret_data.append({
        "wallet": conn.wallet.wallet_name, 
        "partner_name": conn.partner_name, 
        "status":conn.status,
        "type":conn.connection_type,
        "data":conn.connection_data,
        })
    return HttpResponse(json.dumps(ret_data))



def connect(request, form_template='indy/connection/request.html'):
    """Creates a two way connection automatically between two users
    
    Parameters:
    request: the request object recieved by the view
    form_template (str): the path to the file containing the HTML
    request outline

    Returns:
    HttpResponse: output/debugging info
    """
    form = SendConnectionInvitationForm(request.POST)
    if request.method=='POST':
        if not form.is_valid():
            return HttpResponse("form invalid")
        else:
            cd = form.cleaned_data

            #this user's wallet name
            wallet_name = cd.get('wallet_name')
            #double check this user's wallet
            wallet_name_check = request.session['wallet_name']
            assert(wallet_name == wallet_name_check)

            

            # connected user's email and wallet
            this_org = IndyOrganization.objects.filter(wallet=wallet_name).first()
            this_user = get_user_model().objects.filter(wallet=wallet_name).first()

            this = this_org if this_org is not None else this_user
            this_name = this_org.org_name if this_org is not None else this_user.email

            # #partner's email and wallet
            partner_name = cd.get('partner_name')
            partner_org = IndyOrganization.objects.filter(org_name=partner_name).first()
            partner_user = get_user_model().objects.filter(email=partner_name).first()

            partner = partner_org if partner_org is not None else partner_user
            

            # send connection invitation from online user to partner
            my_connection = send_connection_invitation(this.wallet, partner_name)

            connData = json.loads(my_connection.connection_data)['data']

            # send confirmation from partner to online user
            send_connection_confirmation(partner.wallet, 1, this_name, json.dumps(connData['invite_detail']))
            return HttpResponse(partner)
            # set wallet password
            # TODO vcx_config['something'] = raw_password

            # build the connection and get the invitation data back
    else:
        return HttpResponse("hello");            

