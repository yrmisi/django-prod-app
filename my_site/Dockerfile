FROM python:3.12.6-slim

# Set environment variable to ensure unbuffered output
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apt-get update && apt-get install -y python3-dev && rm -rf /var/lib/apt/lists/* && pip install --no-cache-dir --upgrade -r requirements.txt

COPY /my_site .
