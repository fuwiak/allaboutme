# Multi-stage build: Frontend + Backend

# Stage 1: Build frontend (Svelte)
FROM node:20 AS frontend-build
WORKDIR /app/frontend

COPY frontend/package*.json ./
RUN npm ci

COPY frontend/ ./
RUN npm run build

# Stage 2: Backend (Python + FastAPI)
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libmpv1 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ ./backend/

# Copy frontend build to backend static directory
COPY --from=frontend-build /app/frontend/build ./backend/app/static

# Create storage directories
RUN mkdir -p /storage/videos /storage/audio /storage/backgrounds

# Set environment
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

EXPOSE 8000

# Start script
COPY start.sh ./
RUN chmod +x start.sh

CMD ["./start.sh"]

