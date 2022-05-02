import requests
import json


def get_configuration(link_to_config, sapi_token):
    header = {
        'X-StorageApi-Token': sapi_token
    }
    response = requests.get(link_to_config, headers=header)
    if response.status_code != 200:
        resp_json = json.loads(response.text)
        raise ValueError(f"{resp_json.get('error')}")
    return json.loads(response.text).get("configuration")


def get_state(link_to_config, sapi_token):
    header = {
        'X-StorageApi-Token': sapi_token
    }
    response = requests.get(link_to_config, headers=header)
    return json.loads(response.text).get("state")


def push_changes_to_configuration(link_to_config, sapi_token, config):
    header = {
        'X-StorageApi-Token': sapi_token,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    payload = {"configuration": json.dumps(config)}
    response = requests.put(link_to_config, headers=header, data=payload)
    return json.loads(response.text).get("configuration")


def push_changes_to_state(link_to_config, sapi_token, state):
    header = {
        'X-StorageApi-Token': sapi_token,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    payload = {"state": json.dumps(state)}
    response = requests.put(link_to_config, headers=header, data=payload)
    return json.loads(response.text).get("state")


def validate_url(url):
    if "http" not in url:
        raise ValueError("Url missing http")
    if "connection" not in url:
        raise ValueError("Url missing 'connection'")
    if "job" in url:
        raise ValueError("Use link to config not job")
    if "components" not in url:
        raise ValueError("Invalid Url set : missing 'components'")

    if "admin" not in url:
        raise ValueError("Invalid Url set : missing 'admin'")
    if "projects" not in url:
        raise ValueError("Invalid Url set : missing 'projects'")
    if "keboola" not in url:
        raise ValueError("Invalid Url set : missing 'keboola'")

    split_url = url.split("/")
    if len(split_url) < 9:
        raise ValueError("Invalid Url set : too short")


def get_configuration_url(url):
    validate_url(url)
    split_url = url.split("/")
    url = split_url[0:3]
    components_endpoint = ["v2", "storage", "components"]
    component_name = split_url[7]
    configs_ids = split_url[8:]
    url_pieces = url + components_endpoint + [component_name] + ["configs"] + configs_ids
    return "/".join(url_pieces)


def get_stack_url(url):
    split_url = url.split("/")
    keboola_url = split_url[2]
    keboola_url_components = keboola_url.split(".")
    if len(keboola_url_components) == 4:
        keboola_stack = keboola_url_components[1] + "."
    elif len(keboola_url_components) == 5:
        keboola_stack = keboola_url_components[1] + "." + keboola_url_components[2] + "."
    else:
        keboola_stack = ""
    return keboola_stack


def get_component_id_from_url(url):
    split_url = url.split("/")
    return split_url[7]


def get_debug_url_queue1(url):
    validate_url(url)
    keboola_stack = get_stack_url(url)
    component_id = get_component_id_from_url(url)
    debug_url = f"https://syrup.{keboola_stack}keboola.com/docker/{component_id}/debug"
    return debug_url


def get_debug_url_queue2(url):
    validate_url(url)
    keboola_stack = get_stack_url(url)
    debug_url = f"https://queue.{keboola_stack}keboola.com/jobs"
    return debug_url


def get_config_and_row(url):
    split_url = url.split("/")
    configs_ids = split_url[8:]
    config_id = configs_ids[0]
    row_id = None
    if len(configs_ids) == 3:
        row_id = configs_ids[2]
    return config_id, row_id


def get_test_tag_job_url_queue1(url):
    keboola_stack = get_stack_url(url)
    component_id = get_component_id_from_url(url)
    debug_url = f"https://syrup.{keboola_stack}keboola.com/docker/{component_id}/run/tag/test"
    return debug_url


def get_test_tag_job_url_queue2(url):
    keboola_stack = get_stack_url(url)
    test_tag_job_debug_url = f"https://queue.{keboola_stack}keboola.com/jobs"
    return test_tag_job_debug_url


def get_push_state_url(url):
    keboola_stack = get_stack_url(url)
    component_id = get_component_id_from_url(url)
    config, row = get_config_and_row(url)
    row_str = ""
    if row:
        row_str = f"/rows/{row}"
    state_url = f"https://connection.{keboola_stack}keboola.com" \
                f"/v2/storage/components/{component_id}/configs/" \
                f"{config}{row_str}/state"
    return state_url


def get_state_url(url):
    keboola_stack = get_stack_url(url)
    component_id = get_component_id_from_url(url)
    config, row = get_config_and_row(url)
    row_str = ""
    if row:
        row_str = f"/rows/{row}"
    state_url = f"https://connection.{keboola_stack}keboola.com" \
                f"/v2/storage/components/{component_id}/configs/" \
                f"{config}{row_str}"
    return state_url


def update_state_json(state_url, sapi_token, state):
    header = {
        'X-StorageApi-Token': sapi_token,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    payload = {"state": json.dumps(state)}
    response = requests.put(state_url, headers=header, data=payload)
    return json.loads(response.text).get("state")


print(get_debug_url_queue1(
    "https://connection.north-europe.azure.keboola.com/admin/projects/4515/components/kds-team.ex-salesforce-v2/6217711/rows/6217715"))
