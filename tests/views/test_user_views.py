from os import name
import pytest
from app.models.user_model import User
from werkzeug.security import check_password_hash, generate_password_hash


def test_request_signup(client):
    response = client.get("/signup")
    assert "<h1>サインアップ</h1>" in response.data.decode("utf-8")


@pytest.mark.usefixtures("client")
class TestUsersAPI:
    """userAPIのテスト"""

    @pytest.fixture(autouse=True)
    def setup(self, db_session):
        """テストの前にユーザーをセットアップ"""
        self.user = User(name="test user", password="password", email="test@test.com")
        db_session.add(self.user)
        db_session.commit()

    def assert_response(self, expected_keys, response):
        for key in expected_keys:
            assert key in response

    def assert_db_data(self, actual, expect):
        assert actual.id == expect.id
        assert actual.name == expect.name
        assert actual.email == expect.email
        assert check_password_hash(actual.password, expect.password)
        assert actual.is_active == expect.is_active

    def test_create_user(self, client, db_session):
        NAME = "test user"
        PASSWORD = "password"
        EMAIL = "test@example.com"
        response = client.post(
            "/users",
            json={
                "name": NAME,
                "password": PASSWORD,
                "email": EMAIL,
            },
        )
        assert response.status_code == 201

        response_json = response.get_json()
        self.assert_response(["id", "name", "email", "is_active"], response_json)

        actual = db_session.query(User).filter_by(id=response_json["id"]).first()
        self.assert_db_data(
            actual,
            User(
                id=response_json["id"],
                name=NAME,
                email=EMAIL,
                password=PASSWORD,
                is_active=True,
            ),
        )
