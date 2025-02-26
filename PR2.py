from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import asyncio
import threading

# Создаем FastAPI приложение
app = FastAPI()

# Переменная для хранения последнего сообщения
last_message = "Сообщений пока нет."

# Модель для входных данных
class Message(BaseModel):
    text: str

# Маршрут для корневого пути
@app.get("/")
async def root():
    return {"message": last_message}

# Маршрут для обработки сообщения
@app.post("/process_message")
async def process_message(message: Message):
    global last_message
    # Сохраняем последнее сообщение
    last_message = message.text
    # Выводим сообщение в консоль сервера
    print(f"Сервер получил сообщение: {message.text}")
    # Обработка сообщения (например, преобразование в верхний регистр)
    processed_text = message.text.upper()
    return {"original_text": message.text, "processed_text": processed_text}

# Функция для запуска сервера
def run_server():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Функция для отправки сообщения на сервер
async def send_message_to_server(text: str):
    url = "http://127.0.0.1:8000/process_message"
    data = {"text": text}  # Данные для отправки
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data)
        return response.json()

# Основной код
async def main():
    # Запускаем сервер в отдельном потоке
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    # Даем серверу время на запуск
    await asyncio.sleep(1)

    # Бесконечный цикл для отправки сообщений
    while True:
        # Запрашиваем сообщение у пользователя
        user_message = input("Введите сообщение (или 'exit' для выхода): ")
        if user_message.lower() == "exit":
            break

        # Отправляем сообщение на сервер и получаем ответ
        response = await send_message_to_server(user_message)
        print("Ответ от сервера:", response)

# Запуск программы
if __name__ == "__main__":
    asyncio.run(main())