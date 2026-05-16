# backend/Dockerfile
FROM python:3.12-slim
 
WORKDIR /app
 
# Installing system dependencies (needed for psycopg2)
RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*
 
# Copying requirements first.
# If requirements.txt hasn't changed, pip install is skipped on rebuild.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
 
# Copy application code.
COPY . .
 
# Default command (overridden by docker-compose.yml command:)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
