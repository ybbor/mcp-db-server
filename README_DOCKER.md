# MCP Database Server

[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://hub.docker.com/r/souhardyak/mcp-database-server)
[![MCP](https://img.shields.io/badge/MCP-Model%20Context%20Protocol-blue)](https://modelcontextprotocol.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A powerful Model Context Protocol (MCP) server that enables Claude and other AI assistants to interact with databases using natural language queries. Supports SQLite, PostgreSQL, and MySQL with dynamic connection switching.

## ✨ Features

- 🗣️ **Natural Language Queries**: Ask questions in plain English, get SQL results
- 🔄 **Dynamic Database Switching**: Connect to different databases during conversation
- 🛡️ **Security First**: Read-only operations, safe query validation
- 🗃️ **Multi-Database Support**: SQLite, PostgreSQL, MySQL
- 🐳 **Docker Ready**: Official Docker image for easy deployment
- 📊 **Schema Discovery**: Automatic table and column detection
- 🔧 **Flexible Configuration**: Command line, config files, or environment variables

## 🚀 Quick Start

### Using Docker (Recommended)

```bash
# Pull the official image
docker pull souhardyak/mcp-database-server:latest

# Run with SQLite (simplest)
docker run -it --rm \
  -v $(pwd)/data:/data \
  souhardyak/mcp-database-server:latest \
  --database-url "sqlite+aiosqlite:///data/mydb.db"

# Run with PostgreSQL
docker run -it --rm \
  souhardyak/mcp-database-server:latest \
  --database-url "postgresql+asyncpg://user:pass@host:5432/db"
```

### Claude Desktop Integration

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "database-server": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "--volume",
        "/path/to/your/data:/data",
        "souhardyak/mcp-database-server:latest",
        "--database-url",
        "sqlite+aiosqlite:///data/your_database.db"
      ]
    }
  }
}
```

## 📖 Usage Examples

### Natural Language Queries

```
User: "Connect to sqlite+aiosqlite:///students.db"
Claude: ✅ Connected! Found tables: students, courses, enrollments

User: "How many students are enrolled in Computer Science?"
Claude: Found 247 students enrolled in Computer Science courses.

User: "Show me the top 5 students by GPA"
Claude: [Returns formatted table with student data]
```

### Dynamic Database Switching

```
User: "Connect to postgresql://admin:pass@server:5432/sales"
Claude: ✅ Switched to PostgreSQL! Found 8 tables...

User: "What's our total revenue this month?"
Claude: [Queries sales database and returns results]

User: "Now connect back to the students database"
Claude: ✅ Back to student database!
```

## 🛠️ Available Tools

- **`connect_to_database`** - Connect to any database dynamically
- **`query_database`** - Natural language to SQL queries
- **`list_tables`** - Show all available tables
- **`describe_table`** - Get detailed table schema
- **`execute_sql`** - Run direct SQL queries (read-only)
- **`get_connection_examples`** - Show connection URL examples
- **`get_current_database_info`** - Check current connection

## 🔗 Supported Database URLs

```bash
# SQLite
sqlite+aiosqlite:///path/to/database.db
sqlite+aiosqlite:///data/students.db

# PostgreSQL
postgresql+asyncpg://user:password@host:5432/database
postgresql+asyncpg://postgres:admin@localhost:5432/mydb

# MySQL
mysql+aiomysql://user:password@host:3306/database
mysql+aiomysql://root:admin@localhost:3306/mydb
```

## 🐳 Docker Usage

### Basic SQLite Setup

```bash
# Create data directory
mkdir -p ./data

# Run with mounted volume
docker run -it --rm \
  -v $(pwd)/data:/data \
  souhardyak/mcp-database-server:latest \
  --database-url "sqlite+aiosqlite:///data/test.db"
```

### With Docker Compose

```bash
# Clone the repository
git clone https://github.com/Souhar-dya/mcp-database-server
cd mcp-database-server

# Start with SQLite only
docker-compose up mcp-database-server

# Start with PostgreSQL included
docker-compose --profile with-postgres up

# Start with MySQL included
docker-compose --profile with-mysql up
```

### Development Mode

```bash
# Build local image
docker build -t mcp-database-server:dev .

# Run in development
docker run -it --rm \
  -v $(pwd):/app \
  -v $(pwd)/data:/data \
  mcp-database-server:dev \
  --database-url "sqlite+aiosqlite:///data/dev.db"
```

## ⚙️ Configuration

### Command Line Arguments

```bash
python mcp_server.py --help

Options:
  --database-url, -d    Database connection URL
  --config-file, -c     Path to JSON configuration file
```

### Configuration File Example

```json
{
  "type": "postgresql",
  "host": "localhost",
  "port": 5432,
  "user": "postgres",
  "password": "password",
  "database": "mydb"
}
```

### Environment Variables

```bash
export DATABASE_URL="sqlite+aiosqlite:///data/mydb.db"
docker run -it --rm \
  -e DATABASE_URL \
  yourusername/mcp-database-server:latest
```

## 🔒 Security

- **Read-Only Operations**: No DELETE, DROP, UPDATE, or ALTER commands allowed
- **Connection Validation**: All database URLs are validated before connection
- **Non-Root Execution**: Docker container runs as non-root user
- **Input Sanitization**: SQL injection protection built-in

## 🧪 Testing

```bash
# Test the Docker image
docker run --rm souhardyak/mcp-database-server:latest \
  --database-url "sqlite+aiosqlite:///data/test.db" \
  python -c "print('MCP Server Test OK')"

# Health check
docker run --rm souhardyak/mcp-database-server:latest \
  python -c "import asyncio; import sys; sys.path.insert(0, 'app'); from db import DatabaseManager; dm = DatabaseManager(); print('OK' if asyncio.run(dm.test_connection()) else 'FAIL')"
```

## 📝 Example Workflows

### Data Analysis

```
1. "Connect to my sales database"
2. "What are our top-selling products this quarter?"
3. "Show me customer retention rates by region"
4. "Compare this year's performance to last year"
```

### Database Administration

```
1. "Connect to the production database"
2. "List all tables and their sizes"
3. "Check for any tables with missing indexes"
4. "Show me the schema for the users table"
```

### Learning & Education

```
1. "Connect to sqlite+aiosqlite:///school.db"
2. "Show me all students enrolled in 'Introduction to Python'"
3. "What's the average grade for each course?"
4. "Help me practice SQL joins with this data"
```

## 🤝 Contributing

Contributions welcome! Please read our [Contributing Guide](CONTRIBUTING.md) first.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Docker Hub](https://hub.docker.com/r/souhardyak/mcp-database-server)
- [GitHub Repository](https://github.com/Souhar-dya/mcp-database-server)
- [Issues & Support](https://github.com/Souhar-dya/mcp-database-server/issues)

## 🙏 Acknowledgments

- [Anthropic](https://anthropic.com) for the Model Context Protocol
- [FastMCP](https://github.com/jlowin/fastmcp) for the MCP framework
- The open-source community for database drivers and tools

---

**Made with ❤️ for the MCP community**
