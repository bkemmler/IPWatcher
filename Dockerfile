# Stage 1: Build the React frontend
FROM node:18-alpine as builder

WORKDIR /app/frontend

COPY app/frontend/package.json app/frontend/package-lock.json ./
RUN npm install

COPY app/frontend/ .
RUN npm run build

# Stage 2: Build the Python backend
FROM python:3.11-slim

WORKDIR /app

# Install nmap and other dependencies
RUN apt-get update && apt-get install -y nmap curl && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend application code
COPY ./app /app

# Copy the built frontend from the builder stage
COPY --from=builder /app/frontend/build /app/frontend/build

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/healthz || exit 1