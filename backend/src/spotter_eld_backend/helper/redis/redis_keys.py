def get_device_tokens_id(device_type, auth_token):
    """
    Generates the ID used in device authentication token
    @param device_type: the device type 'android', 'ios', 'web',..
    @param auth_token: the authentication token generated to each device
    """

    return "auth_tokens:%s:%s" % (device_type, auth_token)


def get_country_by_deivce_id_key(device_id):
    return "cache:country_code:%s" % device_id


def get_set_forget_password_token(token):
    return "user:forget_password:%s" % token


def get_verify_email_token(token):
    return "user:verify_email:%s" % token


def get_charging_attempt_key(operator, charging_attempt_id):
    return "charging_process:%s:%s" % (operator, charging_attempt_id)


def get_supervisord_key(operator):
    return "charging_process_supervisord:%s" % operator
