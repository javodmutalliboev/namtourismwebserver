FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles
RUN mkdir $APP_HOME/mediafiles
WORKDIR $APP_HOME

COPY requirements.txt $APP_HOME
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

# copy project
COPY . $APP_HOME

RUN pip install --no-cache-dir -r requirements.txt

# Collect static files automatically
RUN python manage.py collectstatic --noinput

EXPOSE 1520
CMD ["gunicorn", "--bind", "0.0.0.0:1520", "namtourism.wsgi:application"]
