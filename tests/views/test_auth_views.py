import pytest


@pytest.mark.usefixtures("client")
class TestLogin:
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

    def assert_user(self, actual, expect):
        assert actual.id == expect.id
        assert actual.name == expect.name
        assert actual.email == expect.email
        assert check_password_hash(actual.password, expect.password)
        assert actual.is_active == expect.is_active

    def test_get_users(self, client):
        """すべてのユーザー情報を取得するテスト"""
        response = client.get("/users")
        response_data = response.data.decode("utf-8")

        assert response.status_code == 200
        self.assert_response([user.name for user in self.users], response_data)
