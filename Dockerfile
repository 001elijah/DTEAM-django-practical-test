   FROM python:3.11-slim

   RUN apt-get update && apt-get install -y \
    libpq-dev \
    build-essential \
    gcc \
    python3-pip \
    libc-dev \
    libpango-1.0-0 \
    libcairo2 \
    libpangoft2-1.0-0 \
    libharfbuzz-subset0 \
    libharfbuzz0b \
    libffi-dev \
    libjpeg-dev \
    libopenjp2-7-dev \
    python3-dev \
    g++ \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

   WORKDIR /app

   COPY pyproject.toml poetry.lock README.md ./
   RUN pip install poetry
   RUN poetry config virtualenvs.create false && poetry install --only main --no-interaction --no-ansi --no-root
   COPY wait-for-it.sh /app/wait-for-it.sh
   RUN chmod +x /app/wait-for-it.sh

   COPY . .

   ENV PYTHONDONTWRITEBYTECODE 1
   ENV PYTHONUNBUFFERED 1

   EXPOSE 8000

   CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
