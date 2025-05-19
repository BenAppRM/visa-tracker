FROM mcr.microsoft.com/playwright/python:v1.52.0-jammy

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    playwright install

CMD ["python", "main.py"]
