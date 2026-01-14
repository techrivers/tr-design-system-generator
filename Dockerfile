FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create generated directory (if needed for local dev)
RUN mkdir -p generated

# Cloud Run sets PORT automatically
EXPOSE 8080

# Run application - Cloud Run automatically sets PORT env var
# Use shell form to properly expand PORT variable
CMD ["sh", "-c", "uvicorn web.app:app --host 0.0.0.0 --port ${PORT:-8080}"]
