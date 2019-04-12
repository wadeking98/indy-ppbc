from django.shortcuts import render

from indy_community.models import *
from .models import *


########################################################################
# Create your views here.
########################################################################
def profile_view(request):
    return render(request, 'imms_demo/imms_profile.html')


def wallet_view(request):
    return render(request, 'imms_demo/imms_wallet.html')


def ha_data_view(request, org):
    return render(request, 'imms_demo/imms_data.html', {'org': org, 'org_role': org.role.name})


def school_data_view(request, org):
    return render(request, 'imms_demo/imms_data.html', {'org': org, 'org_role': org.role.name})


def repo_data_view(request, org):
    return render(request, 'imms_demo/imms_data.html', {'org': org, 'org_role': org.role.name})


# dispatcher
def data_view(request):
    org_id = request.session['ACTIVE_ORG']
    orgs = IndyOrganization.objects.filter(id=org_id).all()

    # let's run separate views per org role
    if orgs[0].role.name == 'HA':
        return ha_data_view(request, orgs[0])
    elif orgs[0].role.name == 'School':
        return school_data_view(request, orgs[0])
    elif orgs[0].role.name == 'Repository':
        return repo_data_view(request, orgs[0])


def ha_issue_credentials(request):
    return render(request, 'indy/form_response.html', {'msg': 'TBD HA issue health id'})


def school_request_health_id(request):
    return render(request, 'indy/form_response.html', {'msg': 'TBD School request health id'})


########################################################################
# auto-processing for received conversations and updated conversation status
########################################################################
def ha_conversation_callback(conversation, prev_type, prev_status, org):
    print("HA conversation callback", prev_type, prev_status, conversation.conversation_type, conversation.status, org)
    # no special handling for HA's
    pass
    

def school_conversation_callback(conversation, prev_type, prev_status, org):
    print("School conversation callback", prev_type, prev_status, conversation.conversation_type, conversation.status, org)

    # if received proof request from Individual (health id's), auto-issue Consent Cred and Imms Proof Request

    # if received Imms Proof, update status

    pass
    

def repo_conversation_callback(conversation, prev_type, prev_status, org):
    print("Repo conversation callback", prev_type, prev_status, conversation.conversation_type, conversation.status, org)

    # if received Imms Proof Request from School, auto-send proof request to Individual

    # if received Proof from Individual, auto-send proof response to School

    pass


def user_conversation_callback(conversation, prev_type, prev_status, user):
    print("User conversation callback", prev_type, prev_status, conversation.conversation_type, conversation.status, user)
    # no special handling for individuals
    pass


# dispatcher
def conversation_callback(conversation, prev_type, prev_status):
    if conversation.wallet.wallet_org:
        org = conversation.wallet.wallet_org
        if org.role.name == 'HA':
            ha_conversation_callback(conversation, prev_type, prev_status, org)
        elif org.role.name == 'School':
            school_conversation_callback(conversation, prev_type, prev_status, org)
        elif org.role.name == 'Repository':
            repo_conversation_callback(conversation, prev_type, prev_status, org)
        else:
            # ignore if it's an unknown org type
            pass
    elif conversation.wallet.wallet_user:
        user = conversation.wallet.wallet_user
        user_conversation_callback(conversation, prev_type, prev_status, user)
    else:
        # ignore un-owned wallets
        pass


