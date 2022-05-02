from src import get_configuration, get_configuration_url, push_changes_to_configuration


def remove_runtime_tag_from_config(config):
    config.pop("runtime", None)
    return config


def revert_tag(url, sapi_token):
    config_url = get_configuration_url(url)
    config = get_configuration(config_url, sapi_token)
    new_config = remove_runtime_tag_from_config(config)
    push_changes_to_configuration(config_url, sapi_token, new_config)
    if new_config == get_configuration(config_url, sapi_token):
        return True
    else:
        return False
