# Официальный легкий образ Python
FROM python:3.11-slim

# Рабочая папка внутри контейнера
WORKDIR /app

# Устанавливаем системные зависимости (если понадобятся)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Копируем и устанавливаем зависимости проекта
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь остальной код проекта внутрь контейнера
COPY . .

# Команда по умолчанию для запуска сервера разработки (или waitress для Windows/продакшна)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]