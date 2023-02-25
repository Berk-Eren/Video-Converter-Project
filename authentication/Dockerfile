FROM python:3.10-slim

LABEL description="Video Converter Authentiation Service"

ENV PYTHONENVBUFFERED 1

WORKDIR /app/authentication

COPY --chown=1000:1000 . /app/authentication

RUN pip install poetry; poetry install

EXPOSE 8000

ENTRYPOINT [ "poetry", "run", "uvicorn", "main:app" ]

CMD ["--host", "0.0.0.0", "--port", "8000"]
