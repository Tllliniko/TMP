from sqlalchemy import create_engine, MetaData
from databases import Database

DATABASE_URL = "sqlite:///./test.db"  # Путь к SQLite-базе данных

database = Database(DATABASE_URL)  # Объект для работы с базой данных
metadata = MetaData()  # Метаданные для таблиц

engine = create_engine(DATABASE_URL)  # Движок для создания таблиц
metadata.create_all(engine)  # Создание всех таблиц