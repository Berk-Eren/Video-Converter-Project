FROM python-3.10:slim

LABEL description="Video Converter Notification Service"

ARG APP_FOLDER=/app/Notification

WORKDIR $APP_FOLDER

COPY . $APP_FOLDER

ENTRYPOINT ["python", "main.py"]