from os import name
import pytest
from app.models.user_model import User
from werkzeug.security import check_password_hash


# htmlを返すエンドポイントのテスト例
def test_request_signup(client):
    response = client.get("/signup")
    assert "<h1>サインアップ</h1>" in response.data.decode("utf-8")


@pytest.mark.usefixtures("client")
class TestUsersAPI:
    """userAPIのテスト"""

    @pytest.fixture(autouse=True)
    def setup(self, db_session):
        """テストの前にユーザーをセットアップ"""
        self.users = [
            User(
                name="test user 1",
                password="password1",
                email="test1@example.com",
                is_active=True,
            ),
            User(
                name="test user 2",
                password="password2",
                email="test2@example.com",
                is_active=True,
            ),
            User(
                name="test user 3",
                password="password3",
                email="test3@example.com",
                is_active=False,
            ),
        ]
        for user in self.users:
            db_session.add(user)
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

    def test_get_users(self, client):
        """すべてのユーザー情報を取得するテスト"""
        response = client.get("/users")

        assert response.status_code == 200

        response_json = response.get_json()
        assert isinstance(response_json, list)  # レスポンスがリストであることを確認
        assert len(response_json) == len(self.users)

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
