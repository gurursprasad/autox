import requests

updated_profile_name = ""


def post_request(api_url, json_payload, timeout=None):
    return requests.post(api_url, json=json_payload, timeout=None)
