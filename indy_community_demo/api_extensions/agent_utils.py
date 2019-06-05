import asyncio
import aiohttp
import json
from os import environ
from pathlib import Path
from tempfile import gettempdir
import random
import uuid

from django.conf import settings

from indy.error import ErrorCode, IndyError

from vcx.api.connection import Connection
from vcx.api.schema import Schema
from vcx.api.credential_def import CredentialDef
from vcx.api.credential import Credential
from vcx.state import State, ProofState
from vcx.api.disclosed_proof import DisclosedProof
from vcx.api.issuer_credential import IssuerCredential
from vcx.api.proof import Proof
from vcx.api.utils import vcx_agent_provision
from vcx.api.vcx_init import vcx_init_with_config
from vcx.common import shutdown

from .models import *
from .utils import *



def send_connection_invitation(wallet, partner_name, initialize_vcx=True):
    """
    Create a VCX Connection Invitation.
    Creates a record for the initator only (receiver is checked in the corresponding view).
    """
    if initialize_vcx:
        try:
            config_json = wallet.wallet_config
            run_coroutine_with_args(vcx_init_with_config, config_json)
        except:
            raise

    # create connection and generate invitation
    try:
       
        connection_to_ = run_coroutine_with_args(Connection.create, partner_name)
        run_coroutine_with_args(connection_to_.connect, '{"use_public_did": true}')
        run_coroutine(connection_to_.update_state)
        invite_details = run_coroutine_with_args(connection_to_.invite_details, False)

        connection_data = run_coroutine(connection_to_.serialize)
        connection_to_.release()
        connection_to_ = None

        # we have two different types of wallets, one class is running in a docker container
        # and I don't know how to access it, the other class is stored in api_extensions,
        # objects of these classes are not considered equal so we must cast them
        
        connection = AgentConnection(
            wallet = wallet,
            partner_name = partner_name,
            invitation = json.dumps(invite_details),
            token = str(uuid.uuid4()),
            connection_type = 'Outbound',
            connection_data = json.dumps(connection_data),
            status = 'Sent')
        connection.save()
    except:
        raise
    finally:
        if initialize_vcx:
            try:
                shutdown(False)
            except:
                raise

    return connection