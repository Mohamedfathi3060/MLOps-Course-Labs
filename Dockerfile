# Use Python 3.12 slim image as base
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install uv for dependency management
RUN pip install uv

# Copy project files
COPY . .

# Install dependencies using uv
RUN uv sync --no-dev

# Expose port 8000 (Litestar default)
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# Run the Litestar server
CMD ["uv", "run", "litestar", "--app", "main:app", "run", "--host", "0.0.0.0"]
