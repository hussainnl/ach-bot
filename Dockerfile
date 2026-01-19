# syntax=docker/dockerfile:1
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /ach_bot

RUN adduser --disabled-password --gecos '' bootuser

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=bootuser:bootuser . .

USER bootuser

CMD ["python", "main.py"]
