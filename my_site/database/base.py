import os
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from my_site.settings import settings

# короче создаем папку для sqlite
BASE_DIR = os.path.dirname(os.path.abspath(__name__))
db_path = os.path.join(BASE_DIR, 'my_site', 'database', 'DB')
if not os.path.exists(db_path):
    os.makedirs(db_path)

Base = declarative_base()

# строка подключения находится в .env (если захотим использовать постгри и т.п.)
# connect_args={'check_same_thread': False} нужен только для sqlite
# если другая бд, то ставим Тру
# в теории больше тут ничего менять не нужно

engine = create_engine(settings.db_url, connect_args={'check_same_thread': False}, echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db_session_local = SessionLocal()
    try:
        yield db_session_local
    finally:
        db_session_local.close()