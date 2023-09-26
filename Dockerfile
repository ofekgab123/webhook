FROM python:3.9-slim-bookworm AS build

WORKDIR /app

COPY requirements.txt /

RUN pip install --no-cache-dir -r /requirements.txt -t /app/lib

COPY . /app/

# ---

FROM gcr.io/distroless/python3-debian12:debug

WORKDIR /app

COPY --from=build /app/ /app/

ENV PYTHONPATH="/app/lib/"

ENTRYPOINT [ "python3","basicWebhook.py" ]