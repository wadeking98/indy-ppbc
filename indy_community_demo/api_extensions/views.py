from django.http import HttpResponseBadRequest, HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, get_user_model, login
from django.urls import reverse
from django.conf import settings

from .forms import *
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
    wallet = get_user_model().objects.filter(wallet_name=wallet_name).first()

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
            partner_name = cd.get('partner_name')

            # get user or org associated with this wallet
            #wallet = wallet_for_current_session(request)
            #wallet_owner = request.session['wallet_owner']

            # get user or org associated with target partner
            target_user = get_user_model().objects.filter(email=partner_name).all()
            # target_org = get_user_model().objects.filter(org_name=partner_name).all()

            # if 0 < len(target_user):
            #     their_wallet = target_user[0].wallet
            # elif 0 < len(target_org):
            #     their_wallet = target_org[0].wallet
            # else:
            #     their_wallet = None

            return HttpResponse(get_user_model().objects)
            # set wallet password
            # TODO vcx_config['something'] = raw_password

            # build the connection and get the invitation data back
    else:
        return HttpResponse("hello");            

def test(request):
    user = get_user_model()
    return HttpResponse(json.dumps(user.objects.all()[0].wallet.wallet_name), content_type="application/json")
