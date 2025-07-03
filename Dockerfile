# Use the official Python image.
FROM python:3.11-slim

# Set the working directory.
WORKDIR /app

# Copy the requirements file and install dependencies.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install nmap.
RUN apt-get update && apt-get install -y nmap && rm -rf /var/lib/apt/lists/*

# Copy the application code.
COPY ./app /app

# Expose the application port.
EXPOSE 8000

# Set the entrypoint.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/healthz || exit 1
