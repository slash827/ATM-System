# Multi-stage build for better security and smaller image size
# Use Python 3.11 (compatible with development environment 3.11.2)
FROM python:3.11-slim-bookworm as builder

# Security: Update system packages and install minimal build dependencies
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    gcc \
    libc6-dev \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean \
    && apt-get autoremove -y

# Create and use virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy and install requirements with security checks
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir --requirement requirements.txt && \
    pip audit --desc --output json || true

# Runtime stage - use Python slim for better compatibility
FROM python:3.11-slim-bookworm

# Security: Create non-root user
RUN useradd --create-home --shell /bin/bash atm

# Set working directory
WORKDIR /app

# Security: Set ownership
RUN chown atm:atm /app

# Copy Python virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code
COPY . .

# Security: Set ownership and switch to non-root user
RUN chown -R atm:atm /app
USER atm

# Security: Set environment to production with secure defaults
ENV ENVIRONMENT=production \
    DEBUG=false \
    LOG_LEVEL=INFO \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app \
    ALLOWED_HOSTS=localhost,127.0.0.1

# Expose port (non-privileged port)
EXPOSE 8000

# Health check (now available with shell)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import httpx; httpx.get('http://localhost:8000/health')" || exit 1

# Run the application
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]