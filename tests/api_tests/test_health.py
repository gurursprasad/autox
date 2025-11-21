class Test_Health_API:
    def test_health(self, session, base_url):
        url = f"{base_url}/health"
        response = session.get(url)
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        data = response.json()
        assert data.get("status") == "ok"
