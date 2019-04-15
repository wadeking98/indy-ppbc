from django.shortcuts import render
from django.conf import settings

from datetime import datetime, date, timedelta
import uuid

import indy_community.models as indy_models
import indy_community.views as indy_views
import indy_community.agent_utils as agent_utils

from .models import *
from .forms import *


# well-known DID's and org names
HA_DID = getattr(settings, "ISLAND_HA_DID", None)
HA_NAME = 'Island Health Authority'
IMMS_REPO_NAME = HA_NAME
SCHOOL_NAME = 'Faber Secondary School'

# credential names
HA_IDENTITY_CREDENIAL = 'HA Identity Certificate'
SCHOOL_IMMS_CONSENT = 'HA Immunization Consent Enablement'

# proof request names
HA_IDENTITY_PROOF = 'HA Proof of Health Identity'
SCHOOL_IMMS_PROOF = 'HA Proof of Immunization'
REPO_CONSENT_PROOF = 'HA Proof of Immunization Consent'

########################################################################
# Create your views here.
########################################################################
def profile_view(request):
    return render(request, 'imms_demo/imms_profile.html')


def wallet_view(request):
    return render(request, 'imms_demo/imms_wallet.html')


def ha_data_view(request, org):
    wallet = indy_views.wallet_for_current_session(request)
    repo_connections = indy_models.AgentConnection.objects.filter(wallet=wallet, status='Active', connection_type='Outbound', partner_name=IMMS_REPO_NAME).all()
    if 0 < len(repo_connections):
        repo_connection = repo_connections[0]
    else:
        repo_connection = None
    user_connections = indy_models.AgentConnection.objects.filter(wallet=wallet, status='Active').exclude(partner_name=IMMS_REPO_NAME).exclude(partner_name=SCHOOL_NAME).all()
    for connection in user_connections:
        print("connection", connection)
        for conversation in connection.agentconversation_set.all():
            print("conversation", conversation)

    return render(request, 'imms_demo/imms_data.html', 
                {'org': org, 
                 'org_role': org.role.name, 
                 'repo_connection': repo_connection,
                 'user_connections': user_connections})


def school_data_view(request, org):
    wallet = indy_views.wallet_for_current_session(request)
    repo_connections = indy_models.AgentConnection.objects.filter(wallet=wallet, status='Active', partner_name=IMMS_REPO_NAME).all()
    if 0 < len(repo_connections):
        repo_connection = repo_connections[0]
    else:
        repo_connection = None
    user_connections = indy_models.AgentConnection.objects.filter(wallet=wallet, status='Active').exclude(partner_name=IMMS_REPO_NAME).all()
    for connection in user_connections:
        print("connection", connection)
        for conversation in connection.agentconversation_set.all():
            print("conversation", conversation)

    return render(request, 'imms_demo/imms_data.html', 
                {'org': org, 
                 'org_role': org.role.name, 
                 'repo_connection': repo_connection,
                 'user_connections': user_connections})


def repo_data_view(request, org):
    return render(request, 'imms_demo/imms_data.html', {'org': org, 'org_role': org.role.name})


# dispatcher
def data_view(request):
    org_id = request.session['ACTIVE_ORG']
    orgs = indy_models.IndyOrganization.objects.filter(id=org_id).all()

    # let's run separate views per org role
    if orgs[0].role.name == 'HA':
        return ha_data_view(request, orgs[0])
    elif orgs[0].role.name == 'School':
        return school_data_view(request, orgs[0])
    elif orgs[0].role.name == 'Repository':
        return repo_data_view(request, orgs[0])


# Health Authority simultaneously issues Health ID (to individual) and Immunization Status (to Imms Repo)
def ha_issue_credentials(request):
    if request.method == 'POST':
        form = IssueHealthIdAndImmsStatusForm(request.POST)
        if not form.is_valid():
            return render(request, 'indy/form_response.html', {'msg': 'Form error', 'msg_txt': str(form.errors)})
        else:
            cd = form.cleaned_data
            connection_id = cd.get('connection_id')
            first_name = cd.get('first_name')
            last_name = cd.get('last_name')
            birth_date = cd.get('birth_date').strftime('%Y-%m-%d')
            health_id = cd.get('health_id')
            health_id_type = cd.get('health_id_type')
            if health_id_type == 'Child':
                health_id_parent = cd.get('health_id_parent')
            else:
                health_id_parent = ''
            issue_date = cd.get('issue_date').strftime('%Y-%m-%d')
            immunization_status = cd.get('immunization_status')
            immunization_status_date = cd.get('immunization_status_date').strftime('%Y-%m-%d')

            wallet = indy_views.wallet_for_current_session(request)
            repo_connections = indy_models.AgentConnection.objects.filter(wallet=wallet, status='Active', connection_type='Outbound', partner_name=IMMS_REPO_NAME).all()
            if 0 < len(repo_connections):
                repo_connection = repo_connections[0]
            else:
                return render(request, 'indy/form_response.html', {'msg': 'Form error', 'msg_txt': "Can't issue credentials, no Immunizations Repository"})
            user_connections = indy_models.AgentConnection.objects.filter(id=connection_id, wallet=wallet, status='Active').all()
            if 0 < len(user_connections):
                user_connection = user_connections[0]
            else:
                return render(request, 'indy/form_response.html', {'msg': 'Form error', 'msg_txt': "Can't issue credentials, no User Connection"})

            if user_connection:
                hi_cred_defs = indy_models.IndyCredentialDefinition.objects.filter(wallet=wallet, creddef_name=HA_IDENTITY_CREDENIAL+'-'+wallet.wallet_name).all()
                if 0 < len(hi_cred_defs):
                    hi_cred_def = hi_cred_defs[0]
                else:
                    return render(request, 'indy/form_response.html', {'msg': 'Form error', 'msg_txt': "Can't issue credentials, no ID Credential Definition"})

                hi_cred_name = first_name + ' ' + last_name
                hi_cred_tag = first_name + ' ' + last_name
                hi_cred_attrs = {
                            "health_id": health_id, 
                            "first_name": first_name, 
                            "last_name": last_name, 
                            "birth_date": birth_date, 
                            "health_id_type": health_id_type, 
                            "parent_health_id": health_id_parent, 
                            "issue_date": issue_date,
                        }

                try:
                    print(" >>> sending health id credential")
                    hi_conversation = agent_utils.send_credential_offer(wallet, user_connection, hi_cred_tag, hi_cred_attrs, hi_cred_def, hi_cred_name)
                except Exception as e:
                    # ignore errors for now
                    print(" >>> Failed to update conversation for", wallet.wallet_name)
                    print(e)
                    return render(request, 'indy/form_response.html', {'msg': 'Failed to update conversation for ' + wallet.wallet_name})

            if repo_connection:
                imms_cred_defs = indy_models.IndyCredentialDefinition.objects.filter(wallet=wallet, creddef_name='HA Immunization Certificate'+'-'+wallet.wallet_name).all()
                if 0 < len(imms_cred_defs):
                    imms_cred_def = imms_cred_defs[0]
                else:
                    return render(request, 'indy/form_response.html', {'msg': 'Form error', 'msg_txt': "Can't issue credentials, no Immunization Credential Definition"})

                imms_cred_name = first_name + ' ' + last_name
                imms_cred_tag = first_name + ' ' + last_name
                imms_cred_attrs = {
                            "health_id": health_id, 
                            "first_name": first_name, 
                            "last_name": last_name, 
                            "birth_date": birth_date, 
                            "immunization_status": immunization_status, 
                            "immunization_status_date": immunization_status_date, 
                        }

                try:
                    print(" >>> sending immunizations certificate")
                    imms_conversation = agent_utils.send_credential_offer(wallet, repo_connection, imms_cred_tag, imms_cred_attrs, imms_cred_def, imms_cred_name)
                except Exception as e:
                    # ignore errors for now
                    print(" >>> Failed to update conversation for", wallet.wallet_name)
                    print(e)
                    return render(request, 'indy/form_response.html', {'msg': 'Failed to update conversation for ' + wallet.wallet_name})

            issued_hi = HealthIdentity(
                            issuer=wallet,
                            health_id=health_id,
                            first_name=first_name,
                            last_name=last_name,
                            birth_date=birth_date,
                            health_id_type=health_id_type,
                            parent_health_id=health_id_parent,
                            issue_date=datetime.now().date(),
                            last_issued=hi_conversation
                        )
            issued_hi.save()

            issued_imms = ImmunizationStatusCertificate(
                            issuer=wallet,
                            health_id=issued_hi,
                            immunization_status=immunization_status,
                            immunization_status_date=immunization_status_date,
                            issue_date=datetime.now().date(),
                            last_issued=imms_conversation
                        )
            issued_imms.save()

            return render(request, 'indy/form_response.html', {'msg': 'Issued Health Identity and Immunizations Credentials'})

    else:
        wallet = indy_views.wallet_for_current_session(request)
        connection_id = request.GET.get('id', None)
        connections = AgentConnection.objects.filter(id=connection_id, wallet=wallet).all()
        connection = connections[0]

        form = IssueHealthIdAndImmsStatusForm(initial={ 'connection_id': connection.id,
                                                        'wallet_name': wallet.wallet_name })
        return render(request, 'imms_demo/ha/issue_id_imms.html', {'form': form})


def school_request_health_id(request):
    if request.method == 'POST':
        form = HealthIdsProofRequestForm(request.POST)
        if not form.is_valid():
            return render(request, 'indy/form_response.html', {'msg': 'Form error', 'msg_txt': str(form.errors)})
        else:
            cd = form.cleaned_data
            connection_id = cd.get('connection_id')
            first_name_child = cd.get('first_name_child')
            last_name_child = cd.get('last_name_child')
            first_name_parent = cd.get('first_name_parent')
            last_name_parent = cd.get('last_name_parent')

            org_id = request.session['ACTIVE_ORG']
            orgs = indy_models.IndyOrganization.objects.filter(id=org_id).all()
            org_role = orgs[0].role

            wallet = indy_views.wallet_for_current_session(request)
            user_connections = indy_models.AgentConnection.objects.filter(id=connection_id, wallet=wallet, status='Active').all()
            if 0 < len(user_connections):
                user_connection = user_connections[0]
            else:
                return render(request, 'indy/form_response.html', {'msg': 'Form error', 'msg_txt': "Can't issue proof, no User Connection"})

            # find proof request
            proof_requests = indy_models.IndyProofRequest.objects.filter(proof_req_name=HA_IDENTITY_PROOF).all()
            if 0 < len(proof_requests):
                proof_request = proof_requests[0]
            else:
                return render(request, 'indy/form_response.html', {'msg': 'Form error', 'msg_txt': "Can't issue proof, proof request not found"})

            # build the proof request and send
            proof_uuid = str(uuid.uuid4())
            proof_name = {
                        'type': HA_IDENTITY_PROOF,
                        'first_name_child': first_name_child,
                        'last_name_child': last_name_child,
                        'first_name_parent': first_name_parent,
                        'last_name_parent': last_name_parent
                    }
            proof_attrs = proof_request.proof_req_attrs
            proof_predicates = proof_request.proof_req_predicates
            proof_attrs = proof_attrs.replace('$HA_DID', HA_DID)
            proof_predicates = proof_predicates.replace('$HA_DID', HA_DID)
            try:
                conversation = agent_utils.send_proof_request(wallet, user_connection, proof_uuid, json.dumps(proof_name), json.loads(proof_attrs), json.loads(proof_predicates))
            except Exception as e:
                # ignore errors for now
                print(" >>> Failed to update conversation for", wallet.wallet_name)
                print(e)
                return render(request, 'indy/form_response.html', {'msg': 'Failed to update conversation for ' + wallet.wallet_name})

            imms_conversation = ImmunizationConversation(
                    wallet=wallet,
                    wallet_role=org_role,
                    health_id_proof=conversation,
                    status='Sent',
                    initiation_date=datetime.now().date()
                )
            imms_conversation.save()

            return render(request, 'indy/form_response.html', {'msg': 'Issued Health Identity Proof Request'})

    else:
        wallet = indy_views.wallet_for_current_session(request)
        connection_id = request.GET.get('id', None)
        connections = AgentConnection.objects.filter(id=connection_id, wallet=wallet).all()
        connection = connections[0]

        form = HealthIdsProofRequestForm(initial={ 'connection_id': connection.id,
                                                        'wallet_name': wallet.wallet_name })
        return render(request, 'imms_demo/school/request_health_id.html', {'form': form})


########################################################################
# auto-processing for received conversations and updated conversation status
########################################################################
def school_auto_receive_proofs(conversation, prev_type, prev_status, org):
    print("school_auto_receive_proofs", prev_type, prev_status, conversation.conversation_type, conversation.status, org)

    # if received Imms Proof Request from School, auto-send proof request to Individual
    if conversation.connection.partner_name == HA_NAME:
        # if received Imms Proof, update status
        print("Proof request from HA")

    else:
        print("Proof request from", conversation.connection.partner_name)

        # TODO check that this is a response to a Health ID check - status etc.

        # find associated Imms Conversation
        imms_conversation = conversation.health_id_proof.get()
        if imms_conversation is None:
            print(" >>> not part of an immunization status protocol, skipping")
            return
        
        # if received proof request from Individual (health id's), auto-issue Consent Cred and Imms Proof Request
        conversation_data = json.loads(conversation.conversation_data)
        proof_data = json.loads(conversation_data['data']['proof']['libindy_proof'])
        proof_request = conversation_data['data']['proof_request']
        proof_req_name = proof_request['proof_request_data']['name']
        try:
            proof_req_name = json.loads(proof_req_name)
        except Exception as e:
            # ignore errors for now
            imms_conversation.status = "Error"
            imms_conversation.msg = "Error in proof_req_name " + proof_req_name
            imms_conversation.save()
            print(" >>> Failed to update conversation,", wallet.wallet_name, imms_conversation.msg)
            print(e)
            return

        # validate data in proof request name
        if proof_req_name['type'] != HA_IDENTITY_PROOF:
            imms_conversation.status = "Error"
            imms_conversation.msg = "Error wrong proof type " + proof_req_name
            imms_conversation.save()
            print(" >>> Failed to update conversation", wallet.wallet_name, imms_conversation.msg)
            return
        if 1 != len(proof_data['proof']['proofs']):
            imms_conversation.status = "Error"
            imms_conversation.msg = "Error data from multiple credentials"
            imms_conversation.save()
            print(" >>> Failed to update conversation", wallet.wallet_name, imms_conversation.msg)
            return

        first_name = proof_data['requested_proof']['revealed_attrs']['first_name']['raw']
        last_name = proof_data['requested_proof']['revealed_attrs']['last_name']['raw']
        health_id = proof_data['requested_proof']['revealed_attrs']['health_id']['raw']
        parent_health_id = proof_data['requested_proof']['revealed_attrs']['parent_health_id']['raw']
        if first_name != proof_req_name['first_name_child'] or last_name != proof_req_name['last_name_child']:
            imms_conversation.status = "Error"
            imms_conversation.msg = "Error child name does not match"
            imms_conversation.save()
            print(" >>> Failed to update conversation", wallet.wallet_name, imms_conversation.msg)
            return

        # ok now construct consent enablement credential (for parent)
        user_connection = conversation.connection
        wallet = user_connection.wallet
        hi_cred_defs = indy_models.IndyCredentialDefinition.objects.filter(wallet=wallet, creddef_name=SCHOOL_IMMS_CONSENT+'-'+wallet.wallet_name).all()
        if 0 < len(hi_cred_defs):
            hi_cred_def = hi_cred_defs[0]
        else:
            imms_conversation.status = "Error"
            imms_conversation.msg = "Error no credential defintion for immunization consent"
            imms_conversation.save()
            print(" >>> Failed to update conversation", wallet.wallet_name, imms_conversation.msg)
            return

        hi_cred_name = first_name + ' ' + last_name
        hi_cred_tag = first_name + ' ' + last_name
        hi_cred_attrs = {
                    "imms_first_name": first_name,
                    "imms_last_name": last_name,
                    "imms_health_id": health_id,
                    "consenting_health_id": parent_health_id,
                    "consent_data": "Consent to release child's immunization status to school",
                    "consent_type": "View Status",
                    "consent_ttl": (datetime.now()+timedelta(days=5)).date().strftime('%Y-%m-%d'),
                }

        try:
            print(" >>> sending immunization consent credential")
            hi_conversation = agent_utils.send_credential_offer(wallet, user_connection, hi_cred_tag, hi_cred_attrs, hi_cred_def, hi_cred_name, initialize_vcx=False)
        except Exception as e:
            imms_conversation.status = "Error"
            imms_conversation.msg = "Error failed to send immunization consent credential"
            imms_conversation.save()
            print(" >>> Failed to update conversation for", wallet.wallet_name)
            print(e)
            return

        imms_conversation.consent_enablement = hi_conversation
        imms_conversation.save()

        # ... and immunization status proof request (for imms repository)
        repo_connections = indy_models.AgentConnection.objects.filter(wallet=wallet, status='Active', partner_name=IMMS_REPO_NAME).all()
        if 0 < len(repo_connections):
            repo_connection = repo_connections[0]
        else:
            imms_conversation.status = "Error"
            imms_conversation.msg = "Error failed to send immunization status proof, no imms repo connection"
            imms_conversation.save()
            print(" >>> Failed to update conversation for", wallet.wallet_name)
            return

        proof_requests = indy_models.IndyProofRequest.objects.filter(proof_req_name=SCHOOL_IMMS_PROOF).all()
        if 0 < len(proof_requests):
            proof_request = proof_requests[0]
        else:
            return render(request, 'indy/form_response.html', {'msg': 'Form error', 'msg_txt': "Can't issue proof, proof request not found"})

        # build the proof request and send
        proof_uuid = str(uuid.uuid4())
        proof_name = {
                    'type': SCHOOL_IMMS_PROOF,
                    'imms_first_name': first_name,
                    'imms_last_name': last_name,
                    'imms_health_id': health_id,
                    'first_name_consent': proof_req_name['first_name_parent'],
                    'last_name_consent': proof_req_name['last_name_parent'],
                    'health_id_consent': parent_health_id
                }
        proof_attrs = proof_request.proof_req_attrs
        proof_predicates = proof_request.proof_req_predicates
        proof_attrs = proof_attrs.replace('$HA_DID', HA_DID)
        proof_predicates = proof_predicates.replace('$HA_DID', HA_DID)
        connection_data = json.loads(repo_connection.connection_data)
        my_did = connection_data['data']['public_did']
        proof_attrs = proof_attrs.replace('$SCHOOL_DID', my_did)
        proof_predicates = proof_predicates.replace('$SCHOOL_DID', my_did)
        try:
            print(" >>> sending immunization status proof request")
            proof_conversation = agent_utils.send_proof_request(wallet, repo_connection, proof_uuid, json.dumps(proof_name), json.loads(proof_attrs), json.loads(proof_predicates), initialize_vcx=False)
        except Exception as e:
            imms_conversation.status = "Error"
            imms_conversation.msg = "Error failed to send immunization status proof request"
            imms_conversation.save()
            print(" >>> Failed to update conversation for", wallet.wallet_name)
            print(e)
            return

        imms_conversation.imms_status_proof = proof_conversation
        imms_conversation.save()
    

def repository_auto_accept_credential_offers(conversation, prev_type, prev_status, org):
    print("repository_auto_accept_credential_offers", prev_type, prev_status, conversation.conversation_type, conversation.status, org)
    connection = conversation.connection
    wallet = connection.wallet

    # if received Imms Credential from HA, auto-accept
    if connection.partner_name == HA_NAME and prev_type is None and prev_status is None:
        print("Credential offer from HA")
        try:
            # note vcx library is initialized since we are in the "process received messages" loop
            conversation = agent_utils.send_credential_request(wallet, connection, conversation, initialize_vcx=False)
        except Exception as e:
            # ignore errors for now
            print(" >>> Failed to update conversation for", wallet.wallet_name)
            print(e)
            pass
    else:
        # ignore others for now
        pass


def repository_auto_receive_credentials(conversation, prev_type, prev_status, org):
    print("repository_auto_receive_credentials", prev_type, prev_status, conversation.conversation_type, conversation.status, org)
    connection = conversation.connection
    wallet = connection.wallet

    # TODO nothing for now ...


def repository_auto_answer_proof_requests(conversation, prev_type, prev_status, org):
    print("repository_auto_answer_proof_requests", prev_type, prev_status, conversation.conversation_type, conversation.status, org)
    connection = conversation.connection
    wallet = connection.wallet

    # if received Imms Proof Request from School, auto-send proof request to Individual
    print("Proof request from", conversation.connection.partner_name)

    # startup an imms_conversation to track this (3-way) conversation
    imms_conversation = ImmunizationConversation(
                    wallet=wallet,
                    wallet_role=org.role,
                    imms_status_proof=conversation,
                    status='Received',
                    initiation_date=datetime.now().date()
                )
    imms_conversation.save()
    print("Saved imms_conversation")

    # validate the data in the proof request name
    print("conversation.conversation_data", conversation.conversation_data)
    conversation_data = json.loads(conversation.conversation_data)
    print("conversation_data", conversation_data)
    proof_request = conversation_data['proof_request_data']
    print("proof_request", proof_request)
    proof_req_name = proof_request['proof_request_data']['name']
    print("proof_req_name", proof_req_name)
    try:
        proof_req_name = json.loads(proof_req_name)
    except Exception as e:
        # ignore errors for now
        imms_conversation.status = "Error"
        imms_conversation.msg = "Error in proof_req_name " + proof_req_name
        imms_conversation.save()
        print(" >>> Failed to update conversation,", wallet.wallet_name, imms_conversation.msg)
        print(e)
        return

    # validate data in proof request name
    print("proof_req_name", proof_req_name)
    if proof_req_name['type'] != SCHOOL_IMMS_PROOF:
        imms_conversation.status = "Error"
        imms_conversation.msg = "Error wrong proof type " + proof_req_name
        imms_conversation.save()
        print(" >>> Failed to update conversation", wallet.wallet_name, imms_conversation.msg)
        return

    # need to send proof request to parent = how to determine which connection is for the Parent?
    print("send proof request to parent for consent ...")
    consenting_health_id = proof_req_name['health_id_consent']
    consenting_identity = HealthIdentity.objects.filter(health_id=consenting_health_id).all()
    if 0 < len(consenting_identity):
        imms_conversation.status = "Error"
        imms_conversation.msg = "Consenting identity not found " + proof_req_name
        imms_conversation.save()
        print(" >>> Failed to update conversation", wallet.wallet_name, imms_conversation.msg)
        return
    consenting_identity = consenting_identity[0]
    consenting_connection = consenting_identity.last_issued.connection

    print("TODO send proof to parent for consent", connection.partner_name)



def repository_auto_receive_proofs(conversation, prev_type, prev_status, org):
    print("repository_auto_receive_proofs", prev_type, prev_status, conversation.conversation_type, conversation.status, org)
    connection = conversation.connection
    wallet = connection.wallet

    # if received Imms Proof Request from School, auto-send proof request to Individual
    print("Proof response received from", conversation.connection.partner_name)

    # need to send proof response to school
    print("TODO send proof response to school ...")



def user_conversation_callback(conversation, prev_type, prev_status, user):
    print("User conversation callback", prev_type, prev_status, conversation.conversation_type, conversation.status, user)
    # no special handling for individuals
    pass


def repository_auto_answer_connections(connection, prev_status):
    print("repository_auto_answer_connections", prev_status, connection.status)


DISPATCH_TABLE = {
    'Org': {
        # Out "HA" is now playing the dual role of "repository" as well
        'HA': {
            # Imms Repository will auto-receive credentials
            'CredentialOffer': repository_auto_accept_credential_offers,
            # no special handling when credentials are received
            'CredentialRequest': repository_auto_receive_credentials,
            # Receive proof request from School, or receive Proof from Parent
            'ProofRequest': {
                'Pending': repository_auto_answer_proof_requests,
                'Accepted': repository_auto_receive_proofs
            }
        },
        'School': {
            # School has no special processing around receipt of credentials
            # Received proof (upon request) from Individual or from Imms Repo
            'ProofRequest': {
                'Accepted': school_auto_receive_proofs
            }
        },
        # "repository" is sitting this one out for now ...
        'Repository': {
            # Imms Repository will auto-receive credentials
            #'CredentialOffer': repository_auto_accept_credential_offers,
            # no special handling when credentials are received
            #'CredentialRequest': repository_auto_receive_credentials,
            # Receive proof request from School, or receive Proof from Parent
            #'ProofRequest': {
            #    'Pending': repository_auto_answer_proof_requests,
            #    'Accepted': repository_auto_receive_proofs
            #},
            #'Connection': repository_auto_answer_connections
        }
    },
    'User': {
        # no special handling for user events
    }
}

# dispatcher
def conversation_callback(conversation, prev_type, prev_status):
    # skip dispatching if nothing has changed
    conversation_type = conversation.conversation_type
    status = conversation.status
    if prev_type and prev_status and (conversation_type == prev_type) and (status == prev_status):
        return

    # determine dispatch function
    dispatch_fn = None
    org = None
    user = None
    if conversation.connection.wallet.wallet_org and 0 < len(conversation.connection.wallet.wallet_org.all()):
        org = conversation.connection.wallet.wallet_org.all()[0]
        role_name = org.role.name
        dispatch = DISPATCH_TABLE['Org']
        if role_name in dispatch:
            dispatch = dispatch[role_name]
        else:
            dispatch = {}
    elif conversation.connection.wallet.wallet_user and 0 < len(conversation.connection.wallet.wallet_user.all()):
        user = conversation.connection.wallet.wallet_user.all()[0]
        dispatch = DISPATCH_TABLE['User']
    else:
        # ignore un-owned wallets
        dispatch = {}

    if conversation_type in dispatch:
        dispatch = dispatch[conversation_type]
        if isinstance(dispatch, dict):
            if status in dispatch:
                dispatch = dispatch[status]
                dispatch_fn = dispatch
        else:
            dispatch_fn = dispatch

    if dispatch_fn:
        print("Dispatching ...")
        if org:
            dispatch(conversation, prev_type, prev_status, org)
        elif user:
            dispatch(conversation, prev_type, prev_status, user)
        else:
            print("Can't dispatch, no org or user found")
    else:
        print("Skipping ...")


# dispatcher
def connection_callback(connection, prev_status):
    print("connection callback", prev_status, connection.status)


