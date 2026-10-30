FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . /app/
RUN echo "🎨 Preparing static files directories..." && \
    mkdir -p /app/staticfiles/static && \
    mkdir -p /app/staticfiles && \
    echo "📁 Removing old static files from staticfiles..." && \
    rm -rf /app/staticfiles/static/* && \
    echo "📋 Copying static files from /app/static to /app/staticfiles/static..." && \
    cp -r /app/static/* /app/staticfiles/static/ 2>/dev/null || true && \
    echo "✅ Static files prepared ($(find /app/staticfiles/static -type f | wc -l) files)"

EXPOSE 8000
