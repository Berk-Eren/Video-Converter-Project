FROM python:3.10-slim

LABEL description="Video Converter Gateway Service"

ENV PYTHONENVBUFFERED 1

ARG APP_FOLDER=/app/gateway
ARG PORT=8001

WORKDIR $APP_FOLDER

COPY --chown=1000:1000 . $APP_FOLDER

RUN pip install poetry; poetry install

EXPOSE $PORT

ENTRYPOINT [ "poetry", "run", "uvicorn", "main:app" ]

CMD ["--host", "0.0.0.0", "--port", "8001"]
