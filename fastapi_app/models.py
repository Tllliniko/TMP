from sqlalchemy import Table, Column, Integer, String
from database import metadata

# Таблица пользователей
users = Table(
    "users", metadata,
    Column("id", Integer, primary_key=True),  # Уникальный идентификатор
    Column("name", String(50)),  # Имя пользователя
    Column("email", String(50), unique=True)  # Уникальный email
)