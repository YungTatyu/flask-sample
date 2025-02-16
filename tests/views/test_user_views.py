import pytest
from werkzeug.security import check_password_hash, generate_password_hash

from app.models.user_model import User


# htmlを返すエンドポイントのテスト例
def test_request_signup(client):
    response = client.get("/signup")
    assert "<h1>サインアップ</h1>" in response.data.decode("utf-8")


@pytest.mark.usefixtures("client")
class TestUsersEndpoints:
    @pytest.fixture(autouse=True)
    def setup(self, db_session):
        """テストの前にユーザーをセットアップ"""
        self.plain_passwords = {"1": "password1", "2": "password2", "3": "password3"}
        self.users = [
            User(
                name="test user 1",
                password=generate_password_hash(self.plain_passwords.get("1")),
                email="test1@example.com",
                is_active=True,
            ),
            User(
                name="test user 2",
                password=generate_password_hash(self.plain_passwords.get("2")),
                email="test2@example.com",
                is_active=True,
            ),
            User(
                name="test user 3",
                password=generate_password_hash(self.plain_passwords.get("3")),
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

    def test_create_user(self, client, db_session):
        """user作成が成功"""
        name = "test user"
        password = "password"
        email = "test@example.com"
        response = client.post(
            "/signup",
            data={
                "name": name,
                "password": password,
                "email": email,
            },
        )
        assert response.status_code == 302

        actual = db_session.query(User).filter_by(name=name).first()
        self.assert_user(
            actual,
            User(
                id=actual.id,  # idのみは取得できない
                name=name,
                email=email,
                password=password,
                is_active=True,
            ),
        )

    def test_create_duplicated_username(self, client, db_session):
        name = "test user 1"  # 重複user
        password = "password"
        email = "test@example.com"
        response = client.post(
            "/signup",
            data={
                "name": name,
                "password": password,
                "email": email,
            },
        )
        response_data = response.data.decode("utf-8")

        assert response.status_code == 409

        # ユーザー数が変更されていないことを確認
        user_count = db_session.query(User).count()
        assert user_count == len(self.users)
        self.assert_response("Name already exists", response_data)

    def test_create_duplicated_email(self, client, db_session):
        name = "test"
        password = "test1@example.com"
        email = "test1@example.com"  # 重複email
        response = client.post(
            "/signup",
            data={
                "name": name,
                "password": password,
                "email": email,
            },
        )
        response_data = response.data.decode("utf-8")

        assert response.status_code == 409

        # ユーザー数が変更されていないことを確認
        user_count = db_session.query(User).count()
        assert user_count == len(self.users)
        self.assert_response("Email already exists", response_data)

    def test_create_user_missing_name(self, client, db_session):
        password = "password"
        email = "test@example.com"
        response = client.post(
            "/signup",
            data={
                "password": password,
                "email": email,
            },
        )
        response_data = response.data.decode("utf-8")

        assert response.status_code == 400

        # ユーザー数が変更されていないことを確認
        user_count = db_session.query(User).count()
        assert user_count == len(self.users)
        self.assert_response("Missing required fields", response_data)

    def test_create_user_missing_password(self, client, db_session):
        name = "name"
        email = "test@example.com"
        response = client.post(
            "/signup",
            data={
                "name": name,
                "email": email,
            },
        )
        response_data = response.data.decode("utf-8")

        assert response.status_code == 400

        # ユーザー数が変更されていないことを確認
        user_count = db_session.query(User).count()
        assert user_count == len(self.users)
        self.assert_response("Missing required fields", response_data)


@pytest.mark.usefixtures("client")
class TestHomePage:
    @pytest.fixture(autouse=True)
    def setup(self, db_session):
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

    def login(self, data, client):
        client.post(
            "/login",
            data=data,
            follow_redirects=True,  # これを使うと cookie を保持してlogin状態をkeepできる
        )

    def test_authenticated_user(self, client):
        self.login({"email": self.user.email, "password": self.password}, client)
        response = client.get("/")
        response_data = response.data.decode("utf-8")

        assert response.status_code == 200
        self.assert_response(f"hello, {self.user.name}", response_data)

    def test_unauthenticated_user(self, client):
        response = client.get("/")

        assert response.status_code == 401
