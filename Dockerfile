FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for better layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Render sets PORT env variable, expose it
EXPOSE ${PORT:-8000}

# Start uvicorn directly, using the PORT environment variable
CMD uvicorn api.main:app --host 0.0.0.0 --port $PORT
