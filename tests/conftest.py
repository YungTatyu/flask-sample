import pytest

from app import create_app
from app.models import db


@pytest.fixture()
def app():
    app = create_app({"SQLALCHEMY_DATABASE_URI": "sqlite://"})  # テスト用DB
    with app.app_context():
        db.create_all()  # テスト用DB作成

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def db_session(app):
    with app.app_context():
        db.session.begin_nested()
        yield db.session  # テスト実行
        db.session.rollback()  # テスト後にデータをロールバック
