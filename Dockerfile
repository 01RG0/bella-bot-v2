# Build Stage for Frontend
FROM node:20-slim as frontend-builder

WORKDIR /app/web
COPY web/package*.json ./
RUN npm ci

COPY web/ ./

# VITE variables need to be available at build time
ARG VITE_DISCORD_CLIENT_ID
ARG VITE_DISCORD_REDIRECT_URI
ARG VITE_API_ALLOW_ORIGIN
ENV VITE_DISCORD_CLIENT_ID=$VITE_DISCORD_CLIENT_ID
ENV VITE_DISCORD_REDIRECT_URI=$VITE_DISCORD_REDIRECT_URI
ENV VITE_API_ALLOW_ORIGIN=$VITE_API_ALLOW_ORIGIN

RUN npm run build

# Final Stage
FROM python:3.11-slim
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends gcc libffi-dev && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY bot/pyproject.toml ./bot/
WORKDIR /app/bot
RUN pip install --upgrade pip
RUN pip install .

# Copy built frontend
COPY --from=frontend-builder /app/web/dist /app/web/dist

# Copy bot code
COPY bot /app/bot

# Copy start script
COPY scripts/render_start.sh /app/scripts/render_start.sh
RUN chmod +x /app/scripts/render_start.sh

# Environment variables
ENV PYTHONUNBUFFERED=1

# Expose port (Render sets PORT env var)
EXPOSE 10000

# Set entrypoint
CMD ["/app/scripts/render_start.sh"]
