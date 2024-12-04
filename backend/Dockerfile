FROM python:3.11-slim

WORKDIR /app
RUN chmod -R 777 /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=3s \
    CMD curl --fail http://localhost:8000/health || exit 1

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
