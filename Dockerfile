# Базовий образ з Python 3.10 (стабільна версія для aiohttp)
FROM python:3.10-slim

# Робоча директорія в контейнері
WORKDIR /app

# Копіюємо файли проекту
COPY requirements.txt .
COPY bot.py .

# Встановлюємо залежності
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Команда запуску бота
CMD ["python", "bot.py"]
