# Multi-stage build for efficient MCP Database Server
FROM python:3.11-slim AS builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies for building
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment
ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy requirements first for better layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Production stage
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

# Install runtime system dependencies
RUN apt-get update && apt-get install -y \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder
COPY --from=builder $VIRTUAL_ENV $VIRTUAL_ENV

# Create app directory and user
RUN groupadd -r mcp && useradd -r -g mcp mcp
WORKDIR /app

# Copy application files
COPY app/ ./app/
COPY mcp_server.py .

# Create data directory for SQLite databases
RUN mkdir -p /data && chown -R mcp:mcp /app /data

# Switch to non-root user
USER mcp

# Set default database path
ENV DATABASE_URL=sqlite+aiosqlite:///data/default.db

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import asyncio; import sys; sys.path.insert(0, 'app'); from db import DatabaseManager; dm = DatabaseManager(); print('OK' if asyncio.run(dm.test_connection()) else 'FAIL')" || exit 1

# Default command runs the MCP server
CMD ["python", "mcp_server.py"]

# Labels for the MCP registry
LABEL org.opencontainers.image.title="MCP Database Server"
LABEL org.opencontainers.image.description="Model Context Protocol server for database interactions with natural language queries"
LABEL org.opencontainers.image.version="1.0.0"
LABEL org.opencontainers.image.authors="Souhardya Kundu <kundusouhardya@gmail.com>"
LABEL org.opencontainers.image.url="https://github.com/Souhar-dya/mcp-db-server"
LABEL org.opencontainers.image.source="https://github.com/Souhar-dya/mcp-db-server"
LABEL org.opencontainers.image.licenses="MIT"
LABEL mcp.server.name="database-server"
LABEL mcp.server.type="database"
LABEL mcp.server.capabilities="query,natural-language,multi-database"