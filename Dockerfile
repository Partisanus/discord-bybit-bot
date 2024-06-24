# Используем базовый образ Python
FROM python:3.10-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы проекта
COPY . .

# Устанавливаем переменные окружения
#ENV TOKEN=YOUR_DISCORD_BOT_TOKEN
#ENV CHANNEL_ID=YOUR_DISCORD_CHANNEL_ID

# Запускаем бота
CMD ["python", "bot.py"]
