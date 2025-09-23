# Database Configuration Guide

The MCP Database Server supports multiple ways to configure your database connection, giving users flexibility to provide database information externally.

## Configuration Methods (in priority order)

### 1. Command Line Arguments (Highest Priority)

```bash
# Direct database URL
python mcp_server.py --database-url "sqlite+aiosqlite:///students.db"
python mcp_server.py -d "postgresql+asyncpg://user:pass@host:port/db"

# Using configuration file
python mcp_server.py --config-file config_postgres.json
python mcp_server.py -c config_sqlite.json
```

### 2. Configuration Files

Create a JSON configuration file with your database settings:

#### SQLite Configuration (`config_sqlite.json`)

```json
{
  "type": "sqlite",
  "database": "students.db",
  "description": "Local SQLite database for student management"
}
```

#### PostgreSQL Configuration (`config_postgres.json`)

```json
{
  "type": "postgresql",
  "host": "localhost",
  "port": 5432,
  "user": "postgres",
  "password": "your_password",
  "database": "students_db",
  "description": "PostgreSQL database connection"
}
```

#### Direct URL Configuration (`config_url.json`)

```json
{
  "database_url": "sqlite+aiosqlite:///students.db",
  "description": "Direct database URL configuration"
}
```

### 3. Environment Variables (Lowest Priority)

Set in `.env` file or system environment:

```bash
DATABASE_URL=sqlite+aiosqlite:///students.db
```

## Claude Desktop Integration

### Method 1: Using Command Line Arguments

Update your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "students-database": {
      "command": "C:\\path\\to\\python.exe",
      "args": [
        "C:\\path\\to\\mcp_server.py",
        "--database-url",
        "sqlite+aiosqlite:///students.db"
      ]
    }
  }
}
```

### Method 2: Using Configuration Files

```json
{
  "mcpServers": {
    "students-database": {
      "command": "C:\\path\\to\\python.exe",
      "args": [
        "C:\\path\\to\\mcp_server.py",
        "--config-file",
        "config_students.json"
      ]
    }
  }
}
```

### Method 3: Using Environment Variables in Claude Config

```json
{
  "mcpServers": {
    "students-database": {
      "command": "C:\\path\\to\\python.exe",
      "args": ["C:\\path\\to\\mcp_server.py"],
      "env": {
        "DATABASE_URL": "sqlite+aiosqlite:///students.db"
      }
    }
  }
}
```

## Database URL Formats

### SQLite

```
sqlite+aiosqlite:///path/to/database.db
sqlite+aiosqlite:///C:/full/path/database.db (Windows)
```

### PostgreSQL

```
postgresql+asyncpg://username:password@host:port/database
postgresql+asyncpg://user:pass@localhost:5432/students_db
```

### MySQL

```
mysql+aiomysql://username:password@host:port/database
mysql+aiomysql://user:pass@localhost:3306/students_db
```

## Usage Examples

### For Students Database

```bash
# Create and use students database
python mcp_server.py -d "sqlite+aiosqlite:///students.db"

# Use existing PostgreSQL
python mcp_server.py -d "postgresql+asyncpg://admin:password@myserver:5432/school_db"

# Use config file
python mcp_server.py -c students_config.json
```

### Creating Custom Configurations

1. **Copy a sample config:**

   ```bash
   cp config_sqlite.json my_database.json
   ```

2. **Edit the configuration:**

   ```json
   {
     "type": "sqlite",
     "database": "/path/to/my/custom.db",
     "description": "My custom database"
   }
   ```

3. **Use it:**
   ```bash
   python mcp_server.py -c my_database.json
   ```

## Security Notes

- Keep database credentials secure
- Use environment variables for sensitive information
- Consider using connection pooling for production
- Validate database permissions before connecting

## Troubleshooting

### Connection Issues

1. Check database URL format
2. Verify database server is running
3. Test connection credentials
4. Check firewall/network settings

### Configuration Issues

1. Validate JSON syntax in config files
2. Check file paths are correct
3. Ensure proper permissions on database files

This flexible configuration system allows users to easily connect to any database without modifying the source code!
