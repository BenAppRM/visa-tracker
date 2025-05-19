FROM mcr.microsoft.com/playwright/python:v1.43.1-jammy

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

CMD ["python", "main.py"]
