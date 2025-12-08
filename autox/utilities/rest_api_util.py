import requests

updated_profile_name = ""


def post_request(api_url, json_payload, timeout=None):
    try:
        return requests.post(api_url, json=json_payload, timeout=timeout)
    except requests.Timeout:
        # Return a Response with 503 for timeouts so callers/tests can assert
        resp = requests.Response()
        resp.status_code = 503
        resp._content = b"Request timed out"
        return resp
    except Exception as e:
        # Return a Response with 502 on unexpected errors
        resp = requests.Response()
        resp.status_code = 502
        resp._content = str(e).encode("utf-8")
        return resp