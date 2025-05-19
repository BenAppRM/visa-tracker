FROM mcr.microsoft.com/playwright/python:latest

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

CMD ["python", "main.py"]
