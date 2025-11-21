import pytest
import requests
import responses

from autox.utilities.rest_api_util import post_request


class Test_MockAPI:
    @pytest.fixture()
    def user_payload(self):
        return {"name": "Guru Prasad", "email": "gurursprasad06@gmail.com", "password": "password123"}

    def test_process_api_success(self, session, base_url, user_payload, mock_service_response):
        api_url = f"{base_url}/v1/user/process"
        service_mock_url = f"{base_url}/v1/data"

        mock_service_response.add(method=responses.POST, url=service_mock_url, json=user_payload, status=200)

        resp = post_request(api_url, user_payload, timeout=None)
        assert resp.status_code == 200
        body = resp.json()
        assert body["status"] == "processed"

    def test_process_api_timeout(self, session, base_url, user_payload, mock_service_response):
        api_url = f"{base_url}/v1/user/process"
        service_mock_url = f"{base_url}/v1/data"

        mock_service_response.add(method=responses.POST, url=service_mock_url, body=requests.exceptions.Timeout())

        resp = post_request(api_url, user_payload, timeout=5)
        assert resp.status_code in (200, 503)

    def test_process_api_handles_500(self, session, base_url, user_payload, mock_service_response):
        api_url = f"{base_url}/v1/user/process"
        service_mock_url = f"{base_url}/v1/data"

        mock_service_response.add(method=responses.POST, url=service_mock_url, status=500)

        resp = post_request(api_url, user_payload, timeout=5)
        assert resp.status_code in (200, 502)
