# mcp-db-server

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

An MCP (Model Context Protocol) server that exposes relational databases (PostgreSQL/MySQL) to AI agents with natural language query support. Transform natural language questions into SQL queries and get structured results.

## 🚀 Features

- **Multi-Database Support**: Works with PostgreSQL and MySQL
- **Natural Language to SQL**: Convert plain English queries to SQL using HuggingFace transformers
- **RESTful API**: Clean FastAPI-based endpoints for database operations
- **Safety First**: Read-only operations with query validation and result limits
- **Docker Ready**: Complete containerization with Docker Compose
- **Production Ready**: Health checks, logging, and error handling
- **AI Agent Friendly**: Designed specifically for AI agent integration

## 📋 API Endpoints

| Endpoint                          | Method | Description                                  |
| --------------------------------- | ------ | -------------------------------------------- |
| `/health`                         | GET    | Health check and service status              |
| `/mcp/list_tables`                | GET    | List all available tables with column counts |
| `/mcp/describe/{table_name}`      | GET    | Get detailed schema for a specific table     |
| `/mcp/query`                      | POST   | Execute natural language queries             |
| `/mcp/tables/{table_name}/sample` | GET    | Get sample data from a table                 |

## 🏃 Quick Start

### Option 1: Docker Compose (Recommended)

1. **Clone and start the services:**

   ```bash
   git clone https://github.com/Souhar-dya/mcp-db-server.git
   cd mcp-db-server
   docker-compose up --build
   ```

2. **Test the endpoints:**

   ```bash
   # Health check
   curl http://localhost:8000/health

   # List tables
   curl http://localhost:8000/mcp/list_tables

   # Describe a table
   curl http://localhost:8000/mcp/describe/customers

   # Natural language query
   curl -X POST "http://localhost:8000/mcp/query" \
     -H "Content-Type: application/json" \
     -d '{"nl_query": "show top 5 customers by total orders"}'
   ```

### Option 2: Local Development

1. **Prerequisites:**

   - Python 3.11+
   - PostgreSQL or MySQL database

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set environment variables:**

   ```bash
   export DATABASE_URL="postgresql+asyncpg://user:password@localhost:5432/dbname"
   # or for MySQL:
   # export DATABASE_URL="mysql+pymysql://user:password@localhost:3306/dbname"
   ```

4. **Run the server:**
   ```bash
   python -m app.server
   ```

## 📊 Sample Database

The project includes a sample database with realistic e-commerce data:

- **customers**: Customer information (10 sample customers)
- **orders**: Order records (17 sample orders)
- **order_items**: Individual items within orders
- **order_summary**: View combining order and customer data

## 🤖 Natural Language Query Examples

The server can understand various types of natural language queries:

```bash
# Get all customers
curl -X POST "http://localhost:8000/mcp/query" \
  -H "Content-Type: application/json" \
  -d '{"nl_query": "show all customers"}'

# Count orders by status
curl -X POST "http://localhost:8000/mcp/query" \
  -H "Content-Type: application/json" \
  -d '{"nl_query": "count orders by status"}'

# Top customers by order value
curl -X POST "http://localhost:8000/mcp/query" \
  -H "Content-Type: application/json" \
  -d '{"nl_query": "top 5 customers by total order amount"}'

# Recent orders
curl -X POST "http://localhost:8000/mcp/query" \
  -H "Content-Type: application/json" \
  -d '{"nl_query": "show recent orders from last week"}'
```

## 🔧 Configuration

### Environment Variables

| Variable       | Description                  | Default                                                          |
| -------------- | ---------------------------- | ---------------------------------------------------------------- |
| `DATABASE_URL` | Full database connection URL | `postgresql+asyncpg://postgres:postgres@localhost:5432/postgres` |
| `DB_HOST`      | Database host                | `localhost`                                                      |
| `DB_PORT`      | Database port                | `5432`                                                           |
| `DB_USER`      | Database username            | `postgres`                                                       |
| `DB_PASSWORD`  | Database password            | `postgres`                                                       |
| `DB_NAME`      | Database name                | `postgres`                                                       |
| `HOST`         | Server host                  | `0.0.0.0`                                                        |
| `PORT`         | Server port                  | `8000`                                                           |

### Database Connection Examples

```bash
# PostgreSQL
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/mydb

# MySQL
DATABASE_URL=mysql+pymysql://user:pass@localhost:3306/mydb

# PostgreSQL with SSL
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/mydb?sslmode=require
```

## 🛡️ Security Features

- **Read-Only Operations**: Only SELECT queries are allowed
- **Query Validation**: Automatic detection and blocking of dangerous SQL operations
- **Result Limiting**: Maximum 50 rows per query (configurable)
- **Input Sanitization**: Protection against SQL injection
- **Safe Defaults**: Secure configuration out of the box

## 🏗️ Architecture

```
mcp-db-server/
├── app/
│   ├── __init__.py          # Package initialization
│   ├── server.py            # FastAPI application and endpoints
│   ├── db.py                # Database connection and operations
│   └── nl_to_sql.py         # Natural language to SQL conversion
├── .github/workflows/
│   └── docker-publish.yml   # CI/CD pipeline
├── docker-compose.yml       # Docker Compose configuration
├── Dockerfile               # Container definition
├── init_db.sql             # Sample database schema and data
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🔄 Model Context Protocol (MCP) Integration

This server is designed to work seamlessly with MCP-compatible AI agents:

1. **Standardized Endpoints**: RESTful API following MCP conventions
2. **Structured Responses**: JSON responses optimized for AI consumption
3. **Error Handling**: Consistent error messages and status codes
4. **Documentation**: OpenAPI/Swagger documentation available at `/docs`

## 🚢 Deployment

### Docker Hub

```bash
# Pull the latest image
docker pull souhardyak/mcp-db-server:latest

# Run with your database
docker run -d \
  -p 8000:8000 \
  -e DATABASE_URL="your_database_url_here" \
  souhardyak/mcp-db-server:latest
```

### Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mcp-db-server
spec:
  replicas: 3
  selector:
    matchLabels:
      app: mcp-db-server
  template:
    metadata:
      labels:
        app: mcp-db-server
    spec:
      containers:
        - name: mcp-db-server
          image: souhardyak/mcp-db-server:latest
          ports:
            - containerPort: 8000
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: db-secret
                  key: url
---
apiVersion: v1
kind: Service
metadata:
  name: mcp-db-server-service
spec:
  selector:
    app: mcp-db-server
  ports:
    - port: 80
      targetPort: 8000
  type: LoadBalancer
```

## 🧪 Testing

### Run Tests Locally

```bash
# Start test database
docker-compose up postgres -d

# Wait for database to be ready
sleep 10

# Run tests
python -m pytest tests/ -v
```

### Manual Testing

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test table listing
curl http://localhost:8000/mcp/list_tables

# Test natural language query
curl -X POST "http://localhost:8000/mcp/query" \
  -H "Content-Type: application/json" \
  -d '{"nl_query": "show me all customers from California"}'
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## � Changelog

### v1.1.0 (2025-09-28) - Async Bug Fix

- **🐛 Fixed**: Resolved `str can't be used in 'await' expression` error in MCP server
- **🔧 Improved**: NLP query processing now works correctly with Claude Desktop integration
- **✅ Enhanced**: Added comprehensive test database setup scripts
- **🚀 Updated**: Docker image rebuilt with bug fixes and updated dependencies

### v1.0.0 (2025-09-25) - Initial Release

- **🎉 Initial**: Full MCP Database Server implementation
- **🌐 Added**: RESTful API with FastAPI
- **🧠 Added**: Natural language to SQL conversion
- **🐳 Added**: Docker containerization and deployment
- **📊 Added**: Multi-database support (PostgreSQL, MySQL, SQLite)

## �🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) for the excellent web framework
- [HuggingFace Transformers](https://huggingface.co/transformers/) for NL to SQL capabilities
- [SQLAlchemy](https://sqlalchemy.org/) for database abstraction
- The Model Context Protocol (MCP) community

## 📞 Support

- 🐛 [Report Issues](https://github.com/Souhar-dya/mcp-db-server/issues)
- 💬 [Discussions](https://github.com/Souhar-dya/mcp-db-server/discussions)
- 📚 [Documentation](https://github.com/Souhar-dya/mcp-db-server/wiki)

---

**⭐ If this project helped you, please consider giving it a star!**
