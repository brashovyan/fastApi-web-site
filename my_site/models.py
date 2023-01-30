from .database.base import Base, engine
from sqlalchemy import Column, String, Integer, Boolean, Numeric, Text


# дальше создаем сущности и указываем связи (почти как в Джанго)
class Publication(Base):
    __tablename__ = 'publication'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), nullable=False)
    content = Column(Text)

# отдельно нужно настроить миграции
# за них отвечает библиотека alembic
# пишем команду alembic init migrations (в самой главной директории (где еще venv)
# настраиваем alembic.ini
# настраиваем migrations/env.py
# сделать миграцию: alembic revision --autogenerate -m "first migration"
# применить миграцию alembic upgrade 9ded4843060e (смотрим в папке versions)
# отменить миграцию alembic downgrade 23252ffwe24

