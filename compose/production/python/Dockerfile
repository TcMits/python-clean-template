FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED 1

# Requirements are installed here to ensure they will be cached.
COPY ./requirements_dev.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt \
    && rm -rf /requirements.txt

COPY ./compose/production/python/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/production/python/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY . /app
WORKDIR /app

ENTRYPOINT ["/entrypoint"]
