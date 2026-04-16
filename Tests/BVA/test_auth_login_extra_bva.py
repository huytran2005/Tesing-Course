class TestAuthenticationBVAExtra:
    """Extra BVA Tests for POST /auth/login (no external HTTP)."""

    def test_auth_login_empty_email(self, client):
        payload = {"email": "", "password": "123456"}
        response = client.post("/auth/login", json=payload)
        assert response.status_code in {400, 401, 422}

    def test_auth_login_empty_password(self, client):
        payload = {"email": "test@example.com", "password": ""}
        response = client.post("/auth/login", json=payload)
        assert response.status_code in {400, 401, 422}

    def test_auth_login_invalid_email_format(self, client):
        payload = {"email": "invalid-email", "password": "123456"}
        response = client.post("/auth/login", json=payload)
        assert response.status_code in {400, 401, 422}

    def test_auth_login_very_long_password(self, client):
        payload = {"email": "test@example.com", "password": "p" * 1000}
        response = client.post("/auth/login", json=payload)
        assert response.status_code in {400, 401, 422}
