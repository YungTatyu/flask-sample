import pytest
from app import create_app
from app.models import db


@pytest.fixture()
def app():
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
        }
    )

    with app.app_context():
        db.create_all()  # テスト用DB作成
    # other setup can go here

    yield app

    with app.app_context():
        db.drop_all()  # テスト終了後にデータを削除


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def db_session(app):
    """テスト用データベースセッション"""
    with app.app_context():
        db.session.begin_nested()
        yield db.session  # テスト実行
        db.session.rollback()  # テスト後にデータをロールバック
