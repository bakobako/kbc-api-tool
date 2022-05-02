from src import get_configuration, get_configuration_url, push_changes_to_configuration


def get_config_json(url, sapi_token):
    config_url = get_configuration_url(url)
    config = get_configuration(config_url, sapi_token)
    return config


def update_configuration_json(url, sapi_token, new_config):
    config_url = get_configuration_url(url)
    push_changes_to_configuration(config_url, sapi_token, new_config)
    if new_config == get_configuration(config_url, sapi_token):
        return True
    else:
        return False
