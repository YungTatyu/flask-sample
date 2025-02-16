import pytest
from werkzeug.security import generate_password_hash

from app.models.user_model import User


@pytest.mark.usefixtures("client")
class TestLogin:
    @pytest.fixture(autouse=True)
    def setup(self, db_session):
        """テストの前にユーザーをセットアップ"""
        self.password = "password1"
        self.user = User(
            name="test user 1",
            password=generate_password_hash(self.password),
            email="test1@example.com",
            is_active=True,
        )

        db_session.add(self.user)
        db_session.commit()

    def assert_response(self, expected_keys, response):
        for key in expected_keys:
            assert key in response

    def test_200(self, client):
        """
        login成功のテスト
        """
        response = client.post(
            "/login", data={"email": self.user.email, "password": self.password}
        )

        assert response.status_code == 302
        # redirect先を確認
        assert response.location == "/"

    def test_400_user_doesnot_exist(self, client):
        """
        存在しないユーザーでlogin
        """
        response = client.post(
            "/login", data={"email": "nonuser", "password": "password"}
        )

        response_data = response.data.decode("utf-8")
        assert response.status_code == 400
        self.assert_response("User does not exist", response_data)

    def test_400_invalid_password(self, client):
        response = client.post(
            "/login", data={"email": self.user.email, "password": "invalidpassword"}
        )

        response_data = response.data.decode("utf-8")

        assert response.status_code == 400
        self.assert_response("Invalid password", response_data)
