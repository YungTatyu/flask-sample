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
