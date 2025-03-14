import os

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Flaskの設定
SECRET_KEY = "dev"

# データベースの設定
DATABASE = os.path.join(BASE_DIR, "app.sqlite")  # SQLiteのパス
SQLALCHEMY_DATABASE_URI = f"sqlite:///{DATABASE}"  # SQLAlchemy用のURI
SQLALCHEMY_TRACK_MODIFICATIONS = False  # パフォーマンス向上のためにオフ
SECRET_KEY = os.getenv("SECRET_KEY")
