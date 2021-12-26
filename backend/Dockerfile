FROM python:3.8.5

RUN mkdir /code
WORKDIR /code
COPY requirements.txt .
RUN python -m pip install --upgrade pip \
    && pip install -r /code/requirements.txt
COPY . .
CMD gunicorn backend.wsgi:application --bind 0.0.0.0:8000
