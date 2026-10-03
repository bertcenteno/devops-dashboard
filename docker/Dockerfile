FROM python:3.12-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libmariadb-dev \
        gcc \
    && rm -rf /var/lib/apt/lists/*

COPY app/api/requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY app/api ./api
COPY app/web ./web

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "api.app:app"]
