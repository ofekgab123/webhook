FROM python:3.9-slim-bookworm

WORKDIR /app

COPY basicWebhook.py requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "python3","basicWebhook.py" ]