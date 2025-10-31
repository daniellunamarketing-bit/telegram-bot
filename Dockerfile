# Беремо стабільну версію Python
FROM python:3.10-slim

# Створюємо робочу директорію всередині контейнера
WORKDIR /app

# Копіюємо всі файли проєкту
COPY . .

# Встановлюємо бібліотеки з requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Вказуємо команду запуску бота
CMD ["python", "bot.py"]
