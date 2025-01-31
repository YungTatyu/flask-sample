import pytest


def test_request_signup(client):
    response = client.get("/signup")
    assert "<h1>サインアップ</h1>" in response.data.decode("utf-8")


@pytest.mark.usefixtures("client")
class TestUsersAPI:
    """userAPIのテスト"""

    def test_edit_user(self, client):
        response = client.post(
            "/users",
            json={
                "name": "test user",
                "password": "password",
                "email": "test@example.com",
            },
        )
        assert response.status_code == 201
