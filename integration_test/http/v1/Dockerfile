FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED 1

# Requirements are installed here to ensure they will be cached.
COPY ./requirements_dev.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt \
    && rm -rf /requirements.txt

COPY . /app
WORKDIR /app

CMD ["pytest", "-v", "./integration_test/http/v1"]
