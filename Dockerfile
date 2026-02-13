# syntax=docker/dockerfile:1
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /ach_bot

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . . 

RUN adduser --disabled-password --gecos '' bootuser && chown -R bootuser /ach_bot
USER bootuser

CMD ["python", "src/main.py"]
