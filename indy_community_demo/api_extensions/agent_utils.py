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