from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import database
import crud
import schemas

# Lifespan-менеджер для обработки событий запуска и завершения
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Подключение к базе данных при запуске
    await database.connect()
    yield
    # Отключение от базы данных при завершении
    await database.disconnect()

# Создание FastAPI-приложения с lifespan
app = FastAPI(lifespan=lifespan)

# Создание пользователя
@app.post("/users/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate):
    user_id = await crud.create_user(user)
    return {"id": user_id, **user.dict()}

# Получение всех пользователей
@app.get("/users/", response_model=list[schemas.User])
async def read_users():
    return await crud.get_users()