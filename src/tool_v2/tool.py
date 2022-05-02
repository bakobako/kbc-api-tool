import requests
import json
from src import get_configuration, get_configuration_url, push_changes_to_configuration, get_debug_url_queue1, \
    get_config_and_row, get_debug_url_queue2, get_component_id_from_url, get_test_tag_job_url_queue1, \
    get_test_tag_job_url_queue2, get_state_url, get_state, get_push_state_url, update_state_json


def run_debug_job(url, sapi_token):
    debug_job_queue1 = run_debug_job_queue1(url, sapi_token)
    if debug_job_queue1.status_code not in [200, 201]:
        run_debug_job_queue2(url, sapi_token)


def run_debug_job_queue1(url, sapi_token):
    debug_url = get_debug_url_queue1(url)
    config, row = get_config_and_row(url)
    config_ids = {
        "config": config
    }
    if row:
        config_ids["row"] = row
    config_id = json.dumps(config_ids)

    return _run_job(debug_url, sapi_token, config_id)


def run_debug_job_queue2(url, sapi_token):
    debug_url = get_debug_url_queue2(url)
    component_id = get_component_id_from_url(url)
    config, row = get_config_and_row(url)
    debug_config = {
        "component": component_id,
        "mode": "debug",
        "config": config
    }
    if row:
        debug_config["configRowIds"] = [row]
    debug_config = json.dumps(debug_config)

    return _run_job(debug_url, sapi_token, debug_config)


def _run_job(debug_url, sapi_token, payload):
    header = {
        'X-StorageApi-Token': sapi_token,
        'Content-Type': 'application/json'
    }
    response = requests.post(debug_url, headers=header, data=payload)
    return response


def run_test_tag_job(url, sapi_token):
    test_tag_job_queue1 = run_test_tag_job_queue1(url, sapi_token)
    if test_tag_job_queue1.status_code not in [200, 201]:
        run_test_tag_job_queue2(url, sapi_token)


def run_test_tag_job_queue1(url, sapi_token):
    test_tag_url = get_test_tag_job_url_queue1(url)
    config, row = get_config_and_row(url)
    config_ids = {
        "config": config
    }
    if row:
        config_ids["row"] = row
    config_id = json.dumps(config_ids)

    return _run_job(test_tag_url, sapi_token, config_id)


def run_test_tag_job_queue2(url, sapi_token):
    test_tag_url = get_test_tag_job_url_queue2(url)
    component_id = get_component_id_from_url(url)
    config, row = get_config_and_row(url)
    test_tag_config = {
        "component": component_id,
        "mode": "run",
        "tag": "test",
        "config": config
    }
    if row:
        test_tag_config["configRowIds"] = [row]
    test_tag_config = json.dumps(test_tag_config)
    return _run_job(test_tag_url, sapi_token, test_tag_config)


def tool_get_config_json(url, sapi_token):
    config_url = get_configuration_url(url)
    config = get_configuration(config_url, sapi_token)
    return config


def tool_update_configuration_json(url, sapi_token, new_config):
    config_url = get_configuration_url(url)
    push_changes_to_configuration(config_url, sapi_token, new_config)
    if new_config == get_configuration(config_url, sapi_token):
        return True
    else:
        return False


def get_state_json(url, sapi_token):
    state_url = get_state_url(url)
    state = get_state(state_url, sapi_token)
    return state


def update_state(url, sapi_token, state):
    state_url = get_push_state_url(url)
    state = update_state_json(state_url, sapi_token, state)
    return state
