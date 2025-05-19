# Dockerfile for visa-tracker with Playwright
FROM mcr.microsoft.com/playwright/python:v1.43.1

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

CMD ["python", "main.py"]
