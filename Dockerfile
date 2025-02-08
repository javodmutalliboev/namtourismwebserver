FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        libpython3-dev \
        libpq-dev \
        python3-tk \
        tk && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY . /app/
RUN pip install --no-cache-dir -r requirements.txt

# Collect static files automatically
RUN python manage.py collectstatic --noinput

EXPOSE 1520
CMD ["gunicorn", "--bind", "0.0.0.0:1520", "namtourism.wsgi:application"]
