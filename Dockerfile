# Multi-stage build for efficient MCP Database Server
FROM python:3.11-slim AS builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies for building
# + unixodbc-dev is needed to compile pyodbc wheels
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    gnupg \
    unixodbc-dev \
    && rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment
ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy requirements first for better layer caching
COPY requirements.txt .

# Install Python dependencies
# Make sure requirements.txt includes: pyodbc, sqlalchemy[asyncio], asyncpg, aiomysql, aiosqlite
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Production stage
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

# --- MSSQL ODBC DRIVER 18 RUNTIME DEPS ---
# Add Microsoft packages repo (Debian 12 bookworm for python:3.11-slim as of 2025)
RUN apt-get update && apt-get install -y curl gnupg apt-transport-https && \
    curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/microsoft-prod.gpg] https://packages.microsoft.com/debian/12/prod bookworm main" > /etc/apt/sources.list.d/microsoft-prod.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y \
      msodbcsql18 \
      # optional but handy for debugging sqlcmd/bcp:
      mssql-tools18 \
      # ODBC driver manager used by msodbcsql18:
      unixodbc \
      # your existing runtime deps:
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

# Default database path (override with MSSQL_URL or DB_* for SQL Server)
ENV DATABASE_URL=sqlite+aiosqlite:///data/default.db

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import asyncio; import sys; sys.path.insert(0, 'app'); from db import DatabaseManager; dm = DatabaseManager(); print('OK' if asyncio.run(dm.test_connection()) else 'FAIL')" || exit 1

# Default command runs the MCP server
CMD ["python", "mcp_server.py"]

# Labels for the MCP registry
LABEL org.opencontainers.image.title="MCP Database Server"
LABEL org.opencontainers.image.description="Model Context Protocol server for database interactions with natural language queries"
LABEL org.opencontainers.image.version="1.1.0"
LABEL org.opencontainers.image.authors="Souhardya Kundu <kundusouhardya@gmail.com>"
LABEL org.opencontainers.image.url="https://github.com/Souhar-dya/mcp-db-server"
LABEL org.opencontainers.image.source="https://github.com/Souhar-dya/mcp-db-server"
LABEL org.opencontainers.image.licenses="MIT"
LABEL mcp.server.name="database-server"
LABEL mcp.server.type="database"
LABEL mcp.server.capabilities="query,natural-language,multi-database"
