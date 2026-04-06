# Streamlit Docker Image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application - only essential files
COPY app.py .

# Copy data and config files - ignore if missing
COPY config.yml . 2>/dev/null || true
COPY styles.css . 2>/dev/null || true
COPY chambres.csv . 2>/dev/null || true
COPY clients.csv . 2>/dev/null || true
COPY reclamations.csv . 2>/dev/null || true
COPY maintenance_tasks.csv . 2>/dev/null || true
COPY logs_sync.csv . 2>/dev/null || true
COPY utilisateurs.json . 2>/dev/null || true
COPY notifications.json . 2>/dev/null || true
COPY hotel_mediterranee.db . 2>/dev/null || true
COPY .env . 2>/dev/null || true
COPY .env.example . 2>/dev/null || true

# Create data dir
RUN mkdir -p .streamlit data

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Run Streamlit
CMD ["python", "-m", "streamlit", "run", "app.py", \
    "--server.port=8501", \
    "--server.address=0.0.0.0", \
    "--server.headless=true", \
    "--server.enableCORS=true"]
