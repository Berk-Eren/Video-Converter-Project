FROM python:3.10-slim


WORKDIR /app/converter

COPY . /app/converter/

RUN pip install poetry; poetry install

ENTRYPOINT poetry run python main.py
